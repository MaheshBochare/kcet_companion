from django.db import models
from core.infrastructure.django_models.Branch_college import CollegeBranch
from core.infrastructure.django_models.Year import Year 
from core.infrastructure.django_models.category import Category
from core.infrastructure.django_models.Round import Round

class SeatMatrix(models.Model):
    college_branch = models.ForeignKey(CollegeBranch, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)

    # Seats
    total_seats = models.PositiveIntegerField()
    filled_seats = models.PositiveIntegerField(default=0)
    available_seats = models.PositiveIntegerField(editable=False)

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "seat_matrix"
        unique_together = ("college_branch", "year", "category", "round")

    def save(self, *args, **kwargs):
        self.available_seats = max(self.total_seats - self.filled_seats, 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.college_branch.code_branch} | {self.category.category_code} | {self.round.round_code} | {self.year.year_code}"
