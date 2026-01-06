from django.db import models
from core.infrastructure.django_models.colleges import College
from core.infrastructure.django_models.Branch import Branch

class CollegeBranch(models.Model):
    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        to_field="college_code",
        db_column="college_code",
        related_name="college_branches"
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        to_field="Branch_Code",
        db_column="Branch_Code",
        related_name="branch_colleges"
    )

    code_branch = models.CharField(max_length=50, unique=True, editable=False)

    class Meta:
        db_table = "college_branch"
        unique_together = ("college", "branch")

    def save(self, *args, **kwargs):
        self.code_branch = f"{self.college.College_code} {self.branch.Branch_Code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code_branch
