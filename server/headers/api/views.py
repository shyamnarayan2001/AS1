from .dataManipulation import InputData, ManipulateData
from rest_framework.views import APIView
from rest_framework.response import Response
from algorithms.api.serializers import ModelSerializer
from algorithms.api.models import Model
from rest_framework import status
import pandas as pd
import json


# --------------------- getHeader ----------------------------- #
# This API will take the input data convert into dataFrame, save it into temporary file,
# if there is no header then add header and return the header
# NOTE :- INPUT
# 1. modelName (String)
# 2. fileType (String) (csv/excel)
# 3. header (String) (y/n)
# 4. file (remote system file path) 
# ------------------------------------------------------------------------ #

class GetHeader(APIView):
    
    def post(self, request, format=None):

        try:
            inputData = InputData()
            fileType = request.data['fileType']

            if not fileType:
                return Response("No filetype recieved")
            
            if fileType == 'csv':
                file_remote = request.FILES['file']
                header = request.data['header']
                flag = inputData.CSV(file_remote, header)

                if flag != 'fine':
                    response_error = {
                        "error" : str(flag)
                    }
                    return Response(response_error, status=status.HTTP_404_NOT_FOUND)

            if fileType == 'excel':
                file_remote = request.FILES['file']
                header = request.data['header']
                flag = inputData.excel(file_remote, header)
                
                if flag != 'fine':
                    response_error = {
                        "error" : str(flag)
                    }
                    return Response(response_error, status=status.HTTP_404_NOT_FOUND)

            df = inputData.df

            # Fetch the column name for display of identifier, features and target
            dataManipulation = ManipulateData()
            header = dataManipulation.fetchColumns(df)

            # Saving the data for future use
            modelName = request.data['modelName']
            path = 'InputDataFrame//' + modelName + '.pkl'
            df.to_pickle(path)  
            return Response(header)

        except Exception as exc:
            response_error = {
                        "error" : str(exc)
                    }
            return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --------------------- GetTestHeader ----------------------------- #
# This API will take the test data as an input, convert into dataFrame, save it into temporary file,
# if there is no header then add header and return the header. It will also take modelName as a input.
#  fetch all the details from dataBase and match identifier, features and target with the test Data.
# if the test Data doesnot match then return error else return headers.
# NOTE :- INPUT
# 1. testName (String)
# 2. fileType (String) (csv/excel)
# 3. header (String) (y/n)
# 4. file (remote system file path) 
# 5. modelName (String) 
# ------------------------------------------------------------------------ #

class GetTestHeader(APIView):
    
    def post(self, request, format=None):

        try:
            inputData = InputData()
            fileType = request.data['fileType']

            if not fileType:
                return Response("No filetype recieved")
            
            if fileType == 'csv':
                file_remote = request.FILES['file']
                header = request.data['header']
                flag = inputData.CSV(file_remote, header)

                if flag != 'fine':
                    response_error = {
                        "error" : str(flag)
                    }
                    return Response(response_error, status=status.HTTP_404_NOT_FOUND)

            if fileType == 'excel':
                file_remote = request.FILES['file']
                header = request.data['header']
                flag = inputData.excel(file_remote, header)
                
                if flag != 'fine':
                    response_error = {
                        "error" : str(flag)
                    }
                    return Response(response_error, status=status.HTTP_404_NOT_FOUND)

            testDf = inputData.df

            # get all the details from database where model name is the user input modelName

            modelName = request.data["modelName"]
    
            try:
                model = Model.objects.get(modelName=modelName)
                serializer = ModelSerializer(model)

                identifier = serializer.data['identifier']
                features = serializer.data['features']
                target = serializer.data['target']

                features = features.split(',')             
               
                # Fetch the column name form input testData to check wheathere it maches with the selected model

                dataManipulation = ManipulateData()
                header = dataManipulation.fetchColumns(testDf)

                for i in features:
                    if (i in header):
                        pass
                    else:
                        response_error = {
                        "error" : "Test data header mismatch with your selected model"
                        }
                        return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                if (target in header):
                    pass
                else:
                    response_error = {
                    "error" : "Test data header mismatch with your selected model"
                    }
                    return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                if (identifier != "n"):
                    if (identifier in header):
                        pass
                    else:
                        response_error = {
                        "error" : "Test data header mismatch with your selected model"
                        }
                        return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # cleaning & saving the data for future use

                testName = request.data['testName']
                path = 'InputDataFrame//' + testName + '.pkl'
                testDf.to_pickle(path)  

                dataManipulation.arrangeDf(testName, identifier, features, target)
                
                response = {
                    "identifier" : identifier,
                    "features" : features,
                    "target" : target,
                    "header" : header
                }
                return Response(response)

            except Model.DoesNotExist:
                response_error = {
                        "error" : "Model Does Not Exist"
                    }
                return Response(response_error, status=status.HTTP_404_NOT_FOUND)

        except Exception as exc:
            response_error = {
                        "error" : str(exc)
                    }
            return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --------------------- GetPredictHeader ----------------------------- #
# This API will take the predict data as an input, convert into dataFrame, save it into temporary file,
# if there is no header then add header and return the header. It will also take modelName as a input.
# fetch all the details from dataBase and match identifier and features  with the predict Data.
# if the predict Data doesnot match then return error else return headers.
# NOTE :- INPUT
# 1. predictName (String)
# 2. fileType (String) (csv/excel)
# 3. header (String) (y/n)
# 4. file (remote system file path) 
# 5. modelName (String) 
# ------------------------------------------------------------------------ #

class GetPredictHeader(APIView):
    
    def post(self, request, format=None):

        try:
            inputData = InputData()
            fileType = request.data['fileType']

            if not fileType:
                return Response("No filetype recieved")
            
            if fileType == 'csv':
                file_remote = request.FILES['file']
                header = request.data['header']
                flag = inputData.CSV(file_remote, header)

                if flag != 'fine':
                    response_error = {
                        "error" : str(flag)
                    }
                    return Response(response_error, status=status.HTTP_404_NOT_FOUND)

            if fileType == 'excel':
                file_remote = request.FILES['file']
                header = request.data['header']
                flag = inputData.excel(file_remote, header)
                
                if flag != 'fine':
                    response_error = {
                        "error" : str(flag)
                    }
                    return Response(response_error, status=status.HTTP_404_NOT_FOUND)

            predictDf = inputData.df

            # get all the details from database where model name is the user input modelName

            modelName = request.data["modelName"]
    
            try:
                model = Model.objects.get(modelName=modelName)
                serializer = ModelSerializer(model)

                identifier = serializer.data['identifier']
                features = serializer.data['features']

                features = features.split(',')             
               
                # Fetch the column name form input testData to check wheathere it maches with the selected model

                dataManipulation = ManipulateData()
                header = dataManipulation.fetchColumns(predictDf)

                for i in features:
                    if (i in header):
                        pass
                    else:
                        response_error = {
                        "error" : "Test data header mismatch with your selected model"
                        }
                        return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                if (identifier != "n"):
                    if (identifier in header):
                        pass
                    else:
                        response_error = {
                        "error" : "Test data header mismatch with your selected model"
                        }
                        return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # cleaning & saving the data for future use

                predictName = request.data['predictName']
                path = 'InputDataFrame//' + predictName + '.pkl'
                predictDf.to_pickle(path)  
                target = "no target"
                dataManipulation.arrangeDf(predictName, identifier, features, target)
                
                response = {
                    "identifier" : identifier,
                    "features" : features,
                    "header" : header
                }
                return Response(response)

            except Model.DoesNotExist:
                response_error = {
                        "error" : "Model Does Not Exist"
                    }
                return Response(response_error, status=status.HTTP_404_NOT_FOUND)

        except Exception as exc:
            response_error = {
                        "error" : str(exc)
                    }
            return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

			
# --------------------- GetHDFSInput ----------------------------- #
# This API will take the predict data as an input, convert into dataFrame, save it into temporary file,
# if there is no header then add header and return the header. It will also take modelName as a input.
# fetch all the details from dataBase and match identifier and features	 with the predict Data.
# if the predict Data doesnot match then return error else return headers.
# NOTE :- INPUT
# 1. modelName (String) 
# 2. host (String) (vsl080hachon02.altimetrik.com)
# 3. port (String) (50070)
# 4. dir (String) (/tmp/altisolve/inputdata/) 
# ------------------------------------------------------------------------ #

class GetHDFSInput(APIView):

	def post(self, request, format=None):

		try:
			inputData = InputData()
			host = request.data['host']
			port = request.data['port']
			dir = request.data['dir']
			flag = inputData.hdfsConnect(host, port, dir)
			if flag != 'fine':
				response_error = {
					"error" : str(flag)
				}
				return Response(response_error, status=status.HTTP_404_NOT_FOUND)

			df = inputData.df

			# Fetch the column name for display of identifier, features and target
			dataManipulation = ManipulateData()
			header = dataManipulation.fetchColumns(df)

			# Saving the data for future use
			modelName = request.data['modelName']
			path = 'InputDataFrame//' + modelName + '.pkl'
			df.to_pickle(path)	
			return Response(header)

		except Exception as exc:
			response_error = {
						"error" : str(exc)
					}
			return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --------------------- GetTestHDFSInput ----------------------------- #
# This API will take the test data as an input, convert into dataFrame, save it into temporary file,
# if there is no header then add header and return the header. It will also take modelName as a input.
#  fetch all the details from dataBase and match identifier, features and target with the test Data.
# if the test Data doesnot match then return error else return headers.
# NOTE :- INPUT
# 1. testName (String)
# 2. host (String) (vsl080hachon02.altimetrik.com)
# 3. port (String) (50070)
# 4. dir (String) (/tmp/altisolve/inputdata/) 
# 5. modelName (String) 
# ------------------------------------------------------------------------ #

class GetTestHDFSInput(APIView):
	
	def post(self, request, format=None):

		try:
			inputData = InputData()
			host = request.data['host']
			port = request.data['port']
			dir = request.data['dir']
			flag = inputData.hdfsConnect(host, port, dir)
			if flag != 'fine':
				response_error = {
					"error" : str(flag)
				}
				return Response(response_error, status=status.HTTP_404_NOT_FOUND)

			testDf = inputData.df

			# get all the details from database where model name is the user input modelName

			modelName = request.data["modelName"]
	
			try:
				model = Model.objects.get(modelName=modelName)
				serializer = ModelSerializer(model)

				identifier = serializer.data['identifier']
				features = serializer.data['features']
				target = serializer.data['target']

				features = features.split(',')             
			   
				# Fetch the column name form input testData to check wheathere it maches with the selected model

				dataManipulation = ManipulateData()
				header = dataManipulation.fetchColumns(testDf)

				for i in features:
					if (i in header):
						pass
					else:
						response_error = {
						"error" : "Test data header mismatch with your selected model"
						}
						return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

				if (target in header):
					pass
				else:
					response_error = {
					"error" : "Test data header mismatch with your selected model"
					}
					return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
				
				if (identifier != "n"):
					if (identifier in header):
						pass
					else:
						response_error = {
						"error" : "Test data header mismatch with your selected model"
						}
						return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
				
				# cleaning & saving the data for future use

				testName = request.data['testName']
				path = 'InputDataFrame//' + testName + '.pkl'
				testDf.to_pickle(path)  

				dataManipulation.arrangeDf(testName, identifier, features, target)
				
				response = {
					"identifier" : identifier,
					"features" : features,
					"target" : target,
					"header" : header
				}
				return Response(response)

			except Model.DoesNotExist:
				response_error = {
						"error" : "Model Does Not Exist"
					}
				return Response(response_error, status=status.HTTP_404_NOT_FOUND)

		except Exception as exc:
			response_error = {
						"error" : str(exc)
					}
			return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --------------------- GetPredictHDFSInput ----------------------------- #
# This API will take the predict data as an input, convert into dataFrame, save it into temporary file,
# if there is no header then add header and return the header. It will also take modelName as a input.
# fetch all the details from dataBase and match identifier and features  with the predict Data.
# if the predict Data doesnot match then return error else return headers.
# NOTE :- INPUT
# 1. predictName (String)
# 2. host (String) (vsl080hachon02.altimetrik.com)
# 3. port (String) (50070)
# 4. dir (String) (/tmp/altisolve/inputdata/) 
# 5. modelName (String) 
# ------------------------------------------------------------------------ #

class GetPredictHDFSInput(APIView):
	
	def post(self, request, format=None):

		try:
			inputData = InputData()
			host = request.data['host']
			port = request.data['port']
			dir = request.data['dir']
			flag = inputData.hdfsConnect(host, port, dir)
			if flag != 'fine':
				response_error = {
					"error" : str(flag)
				}
				return Response(response_error, status=status.HTTP_404_NOT_FOUND)

			predictDf = inputData.df

			# get all the details from database where model name is the user input modelName

			modelName = request.data["modelName"]
	
			try:
				model = Model.objects.get(modelName=modelName)
				serializer = ModelSerializer(model)

				identifier = serializer.data['identifier']
				features = serializer.data['features']

				features = features.split(',')             
			   
				# Fetch the column name form input testData to check wheathere it maches with the selected model

				dataManipulation = ManipulateData()
				header = dataManipulation.fetchColumns(predictDf)

				for i in features:
					if (i in header):
						pass
					else:
						response_error = {
						"error" : "Test data header mismatch with your selected model"
						}
						return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
				
				if (identifier != "n"):
					if (identifier in header):
						pass
					else:
						response_error = {
						"error" : "Test data header mismatch with your selected model"
						}
						return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
				
				# cleaning & saving the data for future use

				predictName = request.data['predictName']
				path = 'InputDataFrame//' + predictName + '.pkl'
				predictDf.to_pickle(path)  
				target = "no target"
				dataManipulation.arrangeDf(predictName, identifier, features, target)
				
				response = {
					"identifier" : identifier,
					"features" : features,
					"header" : header
				}
				return Response(response)

			except Model.DoesNotExist:
				response_error = {
						"error" : "Model Does Not Exist"
					}
				return Response(response_error, status=status.HTTP_404_NOT_FOUND)

		except Exception as exc:
			response_error = {
						"error" : str(exc)
					}
			return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
