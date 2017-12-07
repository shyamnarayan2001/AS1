from rest_framework.views import APIView
from rest_framework.response import Response
from algorithms.api.serializers import ModelSerializer, ModelNameSerializer
from algorithms.api.models import Model
from rest_framework import status

# --------------------- ViewModels ----------------------------- #
# This API will return model details for the requested input modelname.
# NOTE :- INPUT
# 1. modelName (String)
# ------------------------------------------------------------------------ #

class ViewModels(APIView):

	def post(self, request, format=None):

		try:

			modelName = request.data["modelName"]
			queryset = Model.objects.get(modelName = modelName)
			serializer = ModelSerializer(queryset)
			identifier = serializer.data['identifier']
			features = serializer.data['features']
			target = serializer.data['target']
			algorithm_names = serializer.data['algorithm_names']
			features = features.split(',')
			algorithm_names = algorithm_names.split(',')
			response = {
                    "identifier" : identifier,
                    "features" : features,
                    "target" : target,
					"algorithm_names" : algorithm_names
                }
			return Response(response)
		except Exception as exc:
			response_error = {
					"error" : str(exc)
				}
			return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --------------------- ModelList ----------------------------- #
# This API will return all the names of pre build models.
# ------------------------------------------------------------------------ #

class ModelList(APIView):

	def get(self, request, format=None):

		try:
			model = Model.objects.all()
			serializer = ModelNameSerializer(model, many=True)
			return Response(serializer.data)

		except Exception as exc:
			response_error = {
					"error" : str(exc)
				}
			return Response(response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

