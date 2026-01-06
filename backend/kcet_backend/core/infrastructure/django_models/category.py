from django.db import models



class Category(models.Model):
    category_code = models.CharField(max_length=10, unique=True)  # G1, GM, 2AG etc
    category_name = models.CharField(max_length=100, blank=True)

    # Reservation & Eligibility
    reservation_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    min_eligibility_percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    # Classification
    is_general = models.BooleanField(default=False)
    is_reserved = models.BooleanField(default=True)

    # Analytics & Prediction
    demand_weight = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    priority_rank = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "category"
    def __str__(self):
        return self.category_code

