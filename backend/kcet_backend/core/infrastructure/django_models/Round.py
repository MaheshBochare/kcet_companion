from django.db import models

class Round(models.Model):
    round_code = models.CharField(max_length=20, unique=True)  # 1gen, 2gen, 2extgen, 3rd, etc
    round_name = models.CharField(max_length=50, blank=True)   # First Round, Extended Round, etc
    # Analytics / Prediction
    competition_level = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    cutoff_relaxation_factor = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = "round"
    def __str__(self):
        return self.round_code