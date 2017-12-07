from django.db import models
# from datetime import datetime
from django.utils import timezone

class Model(models.Model):
	modelName = models.CharField(max_length=50)
	date = models.DateTimeField(default=timezone.now, blank=True)
	identifier = models.CharField(max_length=50)
	features =  models.CharField(max_length=5000)
	target = models.CharField(max_length=50)
	algorithm_names = models.CharField(max_length=1000)
	max_algorithm_score = models.CharField(max_length=100)
	typeOfData = models.CharField(max_length=100)
	
class Run(models.Model):
	name = models.CharField(max_length=50)
	time = models.DateTimeField(default=timezone.now, blank=True)
	status = models.CharField(max_length=50)
	runType =  models.CharField(max_length=50)
	viewed = models.CharField(max_length=50)