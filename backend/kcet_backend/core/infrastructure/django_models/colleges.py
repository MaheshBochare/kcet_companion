
from django.db import models

class College(models.Model):
    college_code = models.CharField(max_length=10, primary_key=True)
    College_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    approvals=models.CharField(max_length=255)
    naaccrating=models.CharField(max_length=255)
    firstyearfees=models.FloatField(max_length=255)
    averagepackage=models.FloatField(max_length=255)
    highestpackage=models.FloatField(max_length=255)
    Rating=models.FloatField(max_length=255)
    nationalrank=models.IntegerField(max_length=255,blank=True, null=True)

