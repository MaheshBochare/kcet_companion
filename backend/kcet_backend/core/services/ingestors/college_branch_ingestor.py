from django.db import transaction
from core.models import College, Branch, CollegeBranch

class CollegeBranchIngestor:
    def run(self):
        created = 0

        colleges = {c.college_code: c for c in College.objects.all()}
        branches = {b.Branch_Code: b for b in Branch.objects.all()}

        with transaction.atomic():
            for college_code, college in colleges.items():
                for Branch_Code, branch in branches.items():

                    obj, was_created = CollegeBranch.objects.get_or_create(
                        college=college,
                        branch=branch
                    )

                    if was_created:
                        created += 1

        print(f"✅ CollegeBranch ingestion completed. got college  {created} records.")
        return created
