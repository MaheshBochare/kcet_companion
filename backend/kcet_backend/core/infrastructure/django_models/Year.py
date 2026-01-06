from django.db import models

class Year(models.Model):
    year_code = models.PositiveSmallIntegerField(unique=True)  # 24, 23, 22 etc
    year_label = models.CharField(max_length=10, blank=True)   # 2024-25
    # Analytics / Prediction
    competition_index = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


    class Meta:
        db_table = "year_dim"


    def __str__(self):
        return str(self.year_code)
