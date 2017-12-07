from rest_framework.views import APIView
from rest_framework.response import Response
from algorithms.api.serializers import ModelSerializer, RunSerializer
from django.template.loader import render_to_string
from algorithms.api.models import Model, Run
from rest_framework import status
import os

# --------------------- RunList ----------------------------- #
# This API will return list of all the submitted jobs.
# ----------------------------- ----------------------------- #
class RunList(APIView):

    def get(self, request, format=None):
        
        model = Run.objects.all()
        serializer = RunSerializer(model, many=True)
        return Response(serializer.data)   

# --------------------- ViewAnalysis ----------------------------- #
# This API will Show the graph and output CSV file. 
# NOTE :- INPUT
# 1. name (String) (name of test, train or predict)
# 2. runType (String) (Training, Test, Predict)
# ------------------------------------------------------------------------ #
class ViewAnalysis(APIView):

    def post(self, request, format=None):

        try:

            name = request.data["name"]
            runType = request.data["runType"]

            if runType == "Training":

                path = os.getcwd()
                accuracyPlot = '/Output/Graph/Train/' + name + '_AlgoScore.png'
                timePlot = '/Output/Graph/Train/' + name + '_AlgoTime.png'  
                featureImportance = '/Output/Graph/Train/' + name + '_FeatureImportance.png'             
                
                json_response = {
                        "Accuracy Plot" : accuracyPlot,
                        "Time Plot" : timePlot,
                        "Feature Importance" : featureImportance
                    }
                    
                try :

                    alphaAccuracyPlot ='/Output/Graph/Train/' + name + '_AlphaScore.png'                
                    json_response["Alpha Accuracy Plot"] = alphaAccuracyPlot

                except Exception as exc :
                    pass
            
            elif runType == "Test":

                path = os.getcwd()
                accuracyPlot = '/Output/Graph/Test/' + name + '_ModelAccuracy.png'
                featureImportance = '/Output/Graph/Train/' + name + '_FeatureImportance.png'

                json_response = {
                        "Accuracy Plot" : accuracyPlot,
                        #"Feature Importance" : featureImportance
                    }

            elif runType == "Predict":

                path = os.getcwd()
                predict_path = '/Output/Predict/' + name + '_predict.csv'
                print (predict_path)
                featureImportance = '/Output/Graph/Train/' + name + '_FeatureImportance.png'

                json_response = {
                        "Prediction Path" : predict_path,
                       # "Feature Importance" : featureImportance
                    }
            

            # ------------ Update the Run table viewed no to yes -------------------------------
            try:
                model = Run.objects.get(name = name, runType = runType)
                serializer = RunSerializer(model)

                status = serializer.data['status']
                time = serializer.data['time']
                serializer_data = {
                    "name" : name,
                    "time" : time,
                    "status" : status,
                    "runType" :  runType,
                    "viewed" : "yes"
                } 
                model.delete()    
            except Run.DoesNotExist:
                pass
                
            serializer = RunSerializer(data = serializer_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors)

            return Response(json_response)
        except Exception as exc:
            response_error = {
                    "error" : str(exc)
                }
            return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 
