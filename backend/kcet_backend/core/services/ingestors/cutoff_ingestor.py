from django.db import transaction
from core.services.preprocessing.cutoff_preprocessor import CutoffDataPreprocessor
from core.models import College, Branch, CollegeBranch, Category, Round, Year, Cutoff


class CutoffIngestor:

    def __init__(self, file_path, round_type, year):
        self.file_path = file_path
        self.round_type = round_type
        self.year = year

    def run(self):
        print("🚀 Starting cutoff ingestion")

        df = CutoffDataPreprocessor(self.round_type, self.year).transform(self.file_path)

        print("Rows to ingest:", len(df))

        inserted = 0
        skipped = 0

        for _, row in df.iterrows():
            try:
                with transaction.atomic():

                    # 🔑 Use ONLY code_branch from preprocessor
                    college_code, branch_code = row["code_branch"].split("_")

                    college = College.objects.filter(college_code=college_code).first()
                    branch = Branch.objects.filter(Branch_Code=branch_code).first()

                    if not college or not branch:
                        skipped += 1
                        continue

                    cb, _ = CollegeBranch.objects.get_or_create(
                        college=college,
                        branch=branch
                    )

                    category = Category.objects.filter(category_code=row["category"]).first()
                    round_obj = Round.objects.filter(round_code=row["round"]).first()
                    year_obj = Year.objects.filter(year_code=row["year"]).first()

                    if not category or not round_obj or not year_obj:
                        skipped += 1
                        continue

                    Cutoff.objects.update_or_create(
                        college_branch=cb,
                        category=category,
                        round=round_obj,
                        year=year_obj,
                        defaults={"rank": int(row["rank"])}
                    )

                    inserted += 1

            except Exception as e:
                skipped += 1
                print("❌ Row failed:", e)

        print("Inserted:", inserted)
        print(" Skipped:", skipped)
