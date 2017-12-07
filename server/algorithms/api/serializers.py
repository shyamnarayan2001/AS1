from rest_framework import serializers
from .models import Model, Run

class ModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Model
        fields = '__all__'

class ModelNameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Model
        fields = ['modelName']

class RunSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Run
        fields = '__all__'
    