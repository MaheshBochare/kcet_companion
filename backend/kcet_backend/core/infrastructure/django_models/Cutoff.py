from django.db import models

class Cutoff(models.Model):

    college_branch = models.ForeignKey(
        "core.CollegeBranch",
        on_delete=models.CASCADE,
        related_name="cutoffs"
    )

    category = models.ForeignKey(
        "core.Category",
        on_delete=models.CASCADE
    )

    round = models.ForeignKey(
        "core.Round",
        on_delete=models.CASCADE
    )

    year = models.ForeignKey(
        "core.Year",
        on_delete=models.CASCADE
    )

    rank = models.IntegerField(null=True)

    class Meta:
        unique_together = ("college_branch", "category", "round", "year")
