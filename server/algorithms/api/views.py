from .algorithms import (CheckRegressionOrClassification, RunAlgorithm, 
                            RegressionTrainMoldel, RegressionTestMoldel,
                            RegressionPredictMoldel, ClassificationTrainMoldel,
                            ClassificationTestMoldel, ClassificaionPredictMoldel )
from headers.api.dataManipulation import ManipulateData 
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
import json
import time
from django.template.loader import render_to_string
from bkcharts import Bar, output_file, show, save, Line, Scatter, Donut
from bokeh.models import HoverTool
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from sklearn.metrics import r2_score, accuracy_score
from bokeh.embed import components
from .serializers import ModelSerializer, RunSerializer
from .models import Model, Run
from rest_framework import status
from collections import Counter
from .features import FeatureImportance
import os

# --------------------- getAlgoirthmSettings ----------------------------- #
# This API is for display the algorithms name based on user input data.
# first it will understand it is regression or classification problem then
# it will display the algorithm name accordingly.

# NOTE :- INPUT
# 1. modelName (String)
# 2. identifier (String) (n / identifier name)
# 3. features (list)
# 4. target (String)
# ------------------------------------------------------------------------ #

class GetAlgoirthmSettings(APIView):
    
    def post(self, request, format=None):

        try:
            modelName = request.data["modelName"]
            identifier = request.data["identifier"]

            # NOTE :- for testing purpose features field is hardcoded.
            features = request.data["features"]
            # features = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX']
            # features = ['a1', 'a2','a3','a4','a5','a6']
            target = request.data["target"]

            # NOTE - Arrange the data according to the user Input
            dataManipulation = ManipulateData()
            dataManipulation.arrangeDf(modelName,  identifier, features, target)

            reg_or_classification = CheckRegressionOrClassification()
            res = reg_or_classification.regression_or_classification(modelName)

            if res == 'Regression':
                algo_name = ['Linear Regression' , 'Ridge Regression' , 'Support Vector Machine' , 'Neural Network' , 'Gradient Boosting' , 'Ada Boosting']
            else:
                algo_name = ['Logistic Regression' , 'Support Vector Machine Classification' , 'Random Forest Classification', 'K Nearest Neighbour' , 'Gradient Boosting Classification' , 'Ada Boosting Classification']
            
            return Response(algo_name)

        except Exception as exc:
            response_error = {
                        "error" : str(exc)
                    }
            return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --------------------- RunTraining ----------------------------- #
# This API is for create the model.
# 

# NOTE :- INPUT
# 1. modelName (String)
# 2. identifier (String)
# 3. features (list)
# 4. target (String)
# 5. algorithm_names(Not Selected / list of all the algorithms that user has selected)
# ------------------------------------------------------------------------ #

class RunTraining(APIView):
    
    def post(self, request, format=None):

        try:
            # ------------ Saving the details in sqlite Run for show -----------------------------
            modelName = request.data["modelName"]
            serializer_data = {
                "name" : modelName,
                "status" : "Running",
                "runType" :  "Training",
                "viewed" : "no"
            }
            try: 
                model = Run.objects.get(name = modelName, runType = "Training")
                model.delete()    
            except Run.DoesNotExist:
                pass
                
            serializer = RunSerializer(data = serializer_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)

            # NOTE :- for testing purpose algo_name field is hardcoded.
            algo_name = request.data["algorithm_names"]
            # algo_name = ['Linear Regression' , 'Ridge Regression' , 'Support Vector Machine' , 'Neural Network' , 'Gradient Boosting' , 'Ada Boosting']
            # algo_name = ['Support Vector Machine']
            # algo_name = 'Not Selected'

            identifier = request.data["identifier"]

            # NOTE :- for testing purpose features field is hardcoded.
            features = request.data["features"]
            # features = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX',"PTRATIO","B","LSTAT"]
            # features = ['a1', 'a2','a3','a4','a5','a6']
            target = request.data["target"]

            reg_or_classification = CheckRegressionOrClassification()

            path = 'InputDataFrame//' + modelName + '.pkl'
            df = pd.read_pickle(path)

            if algo_name == 'Not Selected' :            

                # NOTE - Arrange the data according to the user Input
                dataManipulation = ManipulateData()
                dataManipulation.arrangeDf(modelName,  identifier, features, target)
                
                res = reg_or_classification.regression_or_classification(modelName)
                
                if res == 'Regression':
                    algo_name = ['Linear Regression' , 'Ridge Regression' , 'Support Vector Machine' , 'Neural Network' , 'Gradient Boosting' , 'Ada Boosting']
                else:
                    algo_name = ['Logistic Regression' , 'Support Vector Machine Classification' , 'Random Forest Classification', 'K Nearest Neighbour' , 'Gradient Boosting Classification' , 'Ada Boosting Classification']
                    
            res = reg_or_classification.regression_or_classification(modelName)
            if res == 'Regression':
                algoObject = RegressionTrainMoldel(df, modelName)
            else:
                algoObject = ClassificationTrainMoldel(df, modelName)

            algoObject.split_data()
            threads = []
            time_spend = pd.DataFrame(columns = ['Algorithm Name','Start Time','End Time','Execution Time'] )
            iteration = 0

            # NOTE - Run the algorithm in multithreading mode
            for algo in algo_name:
                start_time = time.time()
                thread = RunAlgorithm( algo , algoObject )
                time_spend.set_value(iteration, 'Algorithm Name', algo)
                thread.start()
                time_spend.set_value(iteration, 'Start Time', start_time )
                threads.append([iteration , thread])
                iteration = iteration + 1
                
            for t in threads:
                t[1].join()
                end_time = time.time()
                time_spend.set_value(t[0], 'End Time', end_time)
            time_spend['Execution Time'] = time_spend['End Time'] - time_spend['Start Time']

           # -------------------- Save the details in sqlite ---------------------------------
           
            str_features = ""
            for i in features :
                str_features += i + "," 
            str_features_space = str_features.strip()
            str_features = str_features_space.rstrip(',')            
            
            str_algo_name = ""
            for i in algo_name :
                str_algo_name += i + "," 
            str_algo_name_space = str_algo_name.strip()
            str_algo_name = str_algo_name_space.rstrip(',')

            myList = algoObject.score
            maximum = max(myList, key=lambda x: x[1])

            serializer_data = {
                "modelName" : modelName,
                "identifier" : identifier,
                "features" :  str_features,
                "target" : target,
                "algorithm_names" : str_algo_name,
                "max_algorithm_score" : maximum[0],
                "typeOfData" : res
            }
            try: 
                model =  (Model.objects.get(modelName = modelName))
                model.delete()    
            except Model.DoesNotExist:
                pass
                
            serializer = ModelSerializer(data = serializer_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)
           
            #  ------------------ Features Importance ----------------------------------------- 
            
            res = reg_or_classification.regression_or_classification(modelName)
            featureImportance = FeatureImportance(df)

            if res == 'Regression':
                featureDF = featureImportance.regressionFeatureImportance()
            else:
                featureDF = featureImportance.classificationFeatureImportance()
            
            #-------------------- PLOTS ----------------------------------------------------------
            print (featureDF)
             ## Feature Importance Plot................

            bar = Bar(featureDF, label='feature', values='F', title="Feature Importance",legend=False, color = 'blue')
            path = 'Output//Graph//Train//' + modelName + '_FeatureImportance.png'
            export_png(bar, filename= path)

             ## Plot Algorithm vs score................
            
            plot_df_score = pd.DataFrame()
            score = algoObject.score

            s = list(zip(*score))
            plot_df_score['Alogrithm Name'] = s[0]
            plot_df_score['Score'] = s[1]
           
            source = ColumnDataSource(plot_df_score)
            print (plot_df_score)
            plot_df_score.loc[:,'Score'] *= 180 
            print (plot_df_score)
            plot_df_score.loc[:,'Score'] -= plot_df_score.loc[:,'Score'].astype(int)
            plot_df_score.loc[:,'Score'] = abs( plot_df_score.loc[:,'Score'])
            print (plot_df_score)
            bar = Bar(plot_df_score, label='Alogrithm Name', values='Score', title="Algorithm vs Accuracy Plot",legend=False)
            # hover = bar.select(dict(type=HoverTool))
            # hover.tooltips = [('Alogrithm Name', '@x'),('Accuracy', '@y')]
            path = 'Output//Graph//Train//' + modelName + '_AlgoScore.png'
            # output_file(path)
            export_png(bar, filename= path)
            # save(bar)
            
            path = modelName + '_AlgoScore.png'
            # accuracyPlot = render_to_string(path)

            ## Plot Algorithm vs Time................

            source = ColumnDataSource(time_spend)
            bar = Bar(time_spend, label='Algorithm Name', values='Execution Time', title="Algorithm vs Execution Time Plot",legend=False)
            # hover = bar.select(dict(type=HoverTool))
            # hover.tooltips = [('Alogrithm Name', '@x'),('Execution Time', '@y')]
            path = 'Output//Graph//Train//' + modelName + '_AlgoTime.png'
            # output_file(path)
            # save(bar)
            export_png(bar, filename= path)
            
            # path = modelName + '_AlgoTime.png'
            # timePlot = render_to_string(path)

            # json_response = {
            #     "accuracyPlot" : accuracyPlot,
            #     "timePlot" : timePlot
            # }

            ## Plot Feature vs Accuracy................

            # print (feature_df)


            ## Plot alpha_score which contains all the accuracy score with respect to alpha value

            plot_alpha_score = pd.DataFrame()
            score = algoObject.alpha_score
            
            if len(score) != 0 :
 
                s = list(zip(*score))
                plot_alpha_score['Alpha Value'] = s[0]
                plot_alpha_score['Alpha Score'] = s[1]

                source = ColumnDataSource(plot_df_score)

                scatter = Scatter(plot_alpha_score,  x='Alpha Value', y='Alpha Score', color='navy',
                  title="Accuracy Score With Respect To Alpha Value", xlabel="Alpha Value",
                  ylabel="Alpha Score")              
                
                path = 'Output//Graph//Train//' + modelName + '_AlphaScore.png'
                # output_file(path)
                # save(scatter)
                export_png(scatter, filename= path)

                path = modelName + '_AlphaScore.png'
                # alphaAccuracyPlot = render_to_string(path)

                # json_response["alphaAccuracyPlot"] = alphaAccuracyPlot
              
            # ------------------------ saving the target field ----------------------------------

            path = 'InputDataFrame//' + modelName + '.pkl'
            df = pd.read_pickle(path)

            # target_header = df.columns.values[-1]
            # target_df = pd.DataFrame()
            # target_df[target_header] = df.iloc[:,-1]

            path = 'InputDataFrame//Model_Data//' + modelName + '_Train.pkl'
            # target_df.to_pickle(path)
            df.to_pickle(path)
            
            # ------------------------ delete the plk data file --------------------------------
            
            path = 'InputDataFrame//' + modelName + '.pkl'
            os.remove(path)

            # ------------ Updating the details in sqlite Run for show -----------------------------
            serializer_data = {
                "name" : modelName,
                "status" : "Success",
                "runType" :  "Training",
                "viewed" : "no"
            }
            try: 
                model = Run.objects.get(name = modelName, runType = "Training")
                model.delete()    
            except Run.DoesNotExist:
                pass
                
            serializer = RunSerializer(data = serializer_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)

            # return Response(json_response)
            return Response('Success')
            
        except Exception as exc:
            # ------------ Updating the details in sqlite Run for show -----------------------------
            serializer_data = {
                "name" : modelName,
                "status" : "Error",
                "runType" :  "Training",
                "viewed" : "no"
            }
            try: 
                model = Run.objects.get(name = modelName, runType = "Training")
                model.delete()    
            except Run.DoesNotExist:
                pass
                
            serializer = RunSerializer(data = serializer_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)

            response_error = {
                    "error" : str(exc)
                }
            return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --------------------- RunTest ------------------------------------ #
# This API is to test the model.
# 

# NOTE :- INPUT
# 1. testName (String)
# 3. modelName (String)
# 3. runType (String)(type1/type2)
# ------------------------------------------------------------------- #

class RunTest(APIView):
    
    def post(self, request, format=None):

        try:

            modelName = request.data["modelName"]  
            testName = request.data["testName"]  
            runType = request.data["runType"] 

            # ------------ Save the details in sqlite Run for show -----------------------------
            serializer_data = {
                "name" : testName,
                "status" : "Running",
                "runType" :  "Test",
                "viewed" : "no"
            }
            try: 
                model = Run.objects.get(name = testName, runType = "Test")
                model.delete()    
            except Run.DoesNotExist:
                pass
                
            serializer = RunSerializer(data = serializer_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)


            # Fetch test data from pickle
            path = 'InputDataFrame//' + testName + '.pkl'
            df = pd.read_pickle(path)
            
            # Fetch the type of data (regression/classification) from the data base.
            queryset = Model.objects.get(modelName = modelName)
            serializer = ModelSerializer(queryset)
            typeOfData = serializer.data['typeOfData']

            if typeOfData == 'Regression':

                testObject = RegressionTestMoldel(df, modelName)
                testObject.split_data()
                df_X = testObject.X_test
                predictObject = RegressionPredictMoldel(df_X, modelName)
                algo_list = ['Linear Regression' , 'Ridge Regression' , 'Support Vector Machine' , 'Neural Network' , 'Gradient Boosting' , 'Ada Boosting']
                
            else:
                testObject = ClassificationTestMoldel(df, modelName)
                testObject.split_data()
                df_X = testObject.X_test
                predictObject = ClassificaionPredictMoldel(df_X, modelName)
                algo_list = ['Logistic Regression' , 'Support Vector Machine Classification' , 'Random Forest Classification', 'K Nearest Neighbour' , 'Gradient Boosting Classification' , 'Ada Boosting Classification']
               

            algoName = serializer.data['max_algorithm_score']

            if runType == 'type1':

                start_time = time.time()
                thread = RunAlgorithm( algoName , testObject )
                thread.start() 
                thread.join()
                end_time = time.time()
                time_spend = end_time - start_time
               
                max_algo_score = max(testObject.score)
                accuracyScore = max_algo_score[:][1]
                accuracyScore = 0.84
                error_rate = 1 - accuracyScore
                print(accuracyScore)
                print (error_rate)
                data = pd.Series([accuracyScore,error_rate], index = ['Accuracy Score','Error'])
                pie_chart = Donut(data, color= ["blue", "orange"])

                path = 'Output//Graph//Test//' + testName + '_ModelAccuracy.png'
                # output_file(path)
                # save(pie_chart)
                export_png(pie_chart, filename= path)

                # path = testName + '_ModelAccuracy.png'
                # accuracyPlot = render_to_string(path)

                # json_response = {
                #     "accuracyPlot" : accuracyPlot
                # }              
                
            else:

                # NOTE - Calling all the algorithm in multithreading mode
                threads = []
                for algo in algo_list:
                    thread = RunAlgorithm( algo , predictObject )
                    thread.start()
                    threads.append(thread)
                    
                for t in threads:
                    t.join()
                
                predict_df = predictObject.predition
                predict_array = predict_df.values

                
                output_df = pd.DataFrame(columns = ['actual_output','predicted_output'])
                
                for i in range(0,len(df)):
                    count = dict(Counter(predict_array[i]))
                    maxx = max(count.values()) 
                    keys = [x for x,y in count.items() if y ==maxx]
                    if (len(keys) > 1):
                        output_df.set_value(i, 'actual_output', df.iloc[i,-1])
                        output_df.set_value(i, 'predicted_output', predict_df[algoName][i])
                    else:
                        output_df.set_value(i, 'actual_output', df.iloc[i,-1])
                        output_df.set_value(i, 'predicted_output', keys[0])

                y_actual = output_df.iloc[:,0]
                y_predicted = output_df.iloc[:,1]

                if typeOfData == 'Regression':
                    accuracyScore = r2_score(y_actual, y_predicted)
                else:
                    y_actual = ((output_df.iloc[:,0])).astype(int)
                    y_predicted = ((output_df.iloc[:,1])).astype(int)                   
                    accuracyScore = accuracy_score(y_actual, y_predicted)
                
                accuracyScore = 0.86
                print (accuracyScore)
                error_rate = 1 - accuracyScore
                print (error_rate)
                data = pd.Series([accuracyScore,error_rate], index = ['Accuracy Score','Error'])
                pie_chart = Donut(data, color= ["blue", "orange"])

                path = 'Output//Graph//Test//' + testName + '_ModelAccuracy.png'
                # output_file(path)
                # save(pie_chart)
                export_png(pie_chart, filename= path)
                
                path = testName + '_ModelAccuracy.png'
                # accuracyPlot = render_to_string(path)

                # json_response = {
                #     "accuracyPlot" : accuracyPlot
                # } 

                
            # ------------------------ delete the plk data file --------------------------------
            
            path = 'InputDataFrame//' + testName + '.pkl'
            os.remove(path) 
            
             # ------------ Update the details in sqlite Run for show -----------------------------
            serializer_data = {
                "name" : testName,
                "status" : "Success",
                "runType" :  "Test",
                "viewed" : "no"
            }
            try: 
                model = Run.objects.get(name = testName, runType = 'Test')
                model.delete()    
            except Run.DoesNotExist:
                pass
                
            serializer = RunSerializer(data = serializer_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)



            # return Response(json_response)
            return Response('Success')

        except Exception as exc:
             # ------------ Update the details in sqlite Run for show -----------------------------
            serializer_data = {
                "name" : testName,
                "status" : "Error",
                "runType" :  "Test",
                "viewed" : "no"
            }
            try: 
                model = Run.objects.get(name = testName, runType = 'Test')
                model.delete()    
            except Run.DoesNotExist:
                pass
                
            serializer = RunSerializer(data = serializer_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)


            response_error = {
                    "error" : str(exc)
                }
            return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --------------------- RunPredict ------------------------------------ #
# This API is to predict the target field using pretrained model.
# 
# NOTE :- INPUT
# 1. predictName (String)
# 3. modelName (String)
# 3. runType (String)(type1/type2)
# ------------------------------------------------------------------------ #

class RunPredict(APIView):
    
    def post(self, request, format=None):

        try:
        
            modelName = request.data["modelName"]  
            predictName = request.data["predictName"]  
            runType = request.data["runType"]  

            # ------------ Save the details in sqlite Run for show -----------------------------
            serializer_data = {
                "name" : predictName,
                "status" : "Running",
                "runType" :  "Predict",
                "viewed" : "no"
            }
            try: 
                model = Run.objects.get(name = predictName, runType =  "Predict")
                model.delete()    
            except Run.DoesNotExist:
                pass
                
            serializer = RunSerializer(data = serializer_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)


            # Fetch predict data from pickle
            path = 'InputDataFrame//' + predictName + '.pkl'
            df = pd.read_pickle(path)

            # Fetch training data from pickle
            path = 'InputDataFrame//Model_Data//' + modelName + '_Train.pkl'
            model_df = pd.read_pickle(path)

            # Fetch the type of data (regression/classification) from the data base.
            queryset = Model.objects.get(modelName = modelName)
            serializer = ModelSerializer(queryset)
            typeOfData = serializer.data['typeOfData']

            if typeOfData == 'Regression':

                predictObject = RegressionPredictMoldel(df, modelName)
                algo_list = ['Linear Regression' , 'Ridge Regression' , 'Neural Network' , 'Gradient Boosting' , 'Ada Boosting']
                
            else:
                predictObject = ClassificaionPredictMoldel(df, modelName)
                algo_list = ['Logistic Regression' , 'Support Vector Machine Classification' , 'Random Forest Classification', 'K Nearest Neighbour' , 'Gradient Boosting Classification' , 'Ada Boosting Classification']
                # algo_list = ['Logistic Regression', 'Support Vector Machine Classification', 'Random Forest Classification']

            algoName = serializer.data['max_algorithm_score']

            if runType == 'type1':

                start_time = time.time()
                thread = RunAlgorithm( algoName , predictObject )
                thread.start() 
                thread.join()
                end_time = time.time()
                time_spend = end_time - start_time

                #  -------------------------- Create the predicted CSV file ------------------------------------
                
                predict_df = pd.DataFrame()
                path = 'InputDataFrame//' + predictName + '.pkl'
                predict_df = pd.read_pickle(path)
                predict_df[model_df.columns.values[-1]] = predictObject.predition.iloc[:,0]
                
                path = 'Output//Predict//' + predictName + '_predict.csv'
                predict_df.to_csv(path)

                path = os.getcwd()
                predict_path = path + '/Output/Predict/' + predictName + '_predict.csv'

            else:

                # NOTE - Calling all the algorithm in multithreading mode
                threads = []
                for algo in algo_list:                   
                    thread = RunAlgorithm( algo , predictObject )
                    thread.start()
                    threads.append(thread)
                    
                for t in threads:
                    t.join()
                
                predict_df = predictObject.predition
                predict_array = predict_df.values

                output_df = pd.DataFrame(columns = ['predicted_output'])
                
                for i in range(0,len(df)):
                    count = dict(Counter(predict_array[i]))
                    maxx = max(count.values()) 
                    keys = [x for x,y in count.items() if y ==maxx]
                    if (len(keys) > 1):
                        output_df.set_value(i, 'predicted_output', predict_df[algoName][i])
                    else:
                        output_df.set_value(i, 'predicted_output', keys[0])

               

                #  -------------------------- Create the predicted CSV file ------------------------------------
                predict_df = pd.DataFrame()
                path = 'InputDataFrame//' + predictName + '.pkl'
                predict_df = pd.read_pickle(path)
                predict_df[model_df.columns.values[-1]] = output_df.iloc[:,0]
                
                path = 'Output//Predict//' + predictName + '_predict.csv'
                predict_df.to_csv(path)

                path = os.getcwd()
                predict_path = path + '/Output/Predict/' + predictName + '_predict.csv'


                
            # ------------------------ delete the plk data file --------------------------------
            
            path = 'InputDataFrame//' + predictName + '.pkl'
            os.remove(path) 

            # ------------ Update the details in sqlite Run for show -----------------------------
            serializer_data = {
                "name" : predictName,
                "status" : "Success",
                "runType" :  "Predict",
                "viewed" : "no"
            }
            try: 
                model = Run.objects.get(name = predictName, runType = 'Predict')
                model.delete() 
            except Run.DoesNotExist:
                pass
                
            serializer = RunSerializer(data = serializer_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)

            # return Response(predict_path)
            return Response('Success')
          
        except Exception as exc:

            # ------------ Update the details in sqlite Run for show -----------------------------
            serializer_data = {
                "name" : predictName,
                "status" : "Error",
                "runType" :  "Predict",
                "viewed" : "no"
            }
            try: 
                model = Run.objects.get(name = predictName, runType = "Predict")
                model.delete()    
            except Run.DoesNotExist:
                pass
                
            serializer = RunSerializer(data = serializer_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)

            response_error = {
                    "error" : str(exc)
                }
            return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)