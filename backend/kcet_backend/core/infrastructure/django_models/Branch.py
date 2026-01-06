from django.db import models

class Branch(models.Model):
    Branch_Code = models.CharField(max_length=10, primary_key=True)
    Branch_Name = models.CharField(max_length=255)
    Stream=models.CharField(max_length=255)
    Degree_Type = models.CharField(max_length=50)   # BE / BTech / BArch
    Duration_Years = models.PositiveSmallIntegerField(default=4)
    Is_Core_Branch = models.BooleanField(default=False)   # CSE, ECE, ME, CE
    Is_Emerging_Branch = models.BooleanField(default=False)  # AI, DS, Cyber, AIML
    Popularity_Rank = models.PositiveIntegerField(blank=True, null=True)
    Demand_Score = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    Is_Active = models.BooleanField(default=True)
    Created_At = models.DateTimeField(auto_now_add=True)
    Updated_At = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.Branch_Name} ({self.Branch_Code})"