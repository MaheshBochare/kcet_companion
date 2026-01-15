from django.db import transaction
from core.models import College

class CollegeIngestionService:

    @staticmethod
    @transaction.atomic
    def refresh_colleges(df):
        count = 0
        for _, row in df.iterrows():
            College.objects.update_or_create(
                college_code=row["college_code"],
                defaults={
                    "College_name": row["College_Name"],
                    "location": row["Location"],
                    "approvals": row["Approvals"],
                    "naaccrating": row["NAAC_Grade"],
                    "firstyearfees": row["First_Year_Fees"],
                    "averagepackage": row["Avg_Package"],
                    "highestpackage": row["Highest_Package"],
                    "Rating": row["Rating"],
                    "nationalrank": row["National_Ranking"],
                }
            )
            count += 1
        return count
