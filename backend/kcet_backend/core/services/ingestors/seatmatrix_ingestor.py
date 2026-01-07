from django.db import transaction
from core.services.preprocessing.seat_matrix import SeatMatrixPreprocessor
from core.models import College, Branch, CollegeBranch, SeatMatrix, Year, Category, Round


class SeatMatrixIngestor:

    def __init__(self, file_path, round_code, year_code):
        self.file_path = file_path
        self.round_code = round_code
        self.year_code = year_code

    def run(self):
        print("🚀 Starting Seat Matrix ingestion")

        df = SeatMatrixPreprocessor(self.file_path).process()
        print("Rows extracted:", len(df))

        inserted = 0
        skipped = 0

        for _, row in df.iterrows():
            try:
                with transaction.atomic():

                    college_code, branch_code = row["code_branch"].split("_")

                    college = College.objects.filter(college_code=college_code).first()
                    if not college:
                        print("Missing College:", college_code)
                        skipped += 1
                        continue

                    branch = Branch.objects.filter(Branch_Code=branch_code).first()
                    if not branch:
                        print("Missing Branch:", branch_code)
                        skipped += 1
                        continue

                    cb, _ = CollegeBranch.objects.get_or_create(college=college, branch=branch)

                    year = Year.objects.filter(year_code=self.year_code).first()
                    if not year:
                        print("Missing Year:", self.year_code)
                        skipped += 1
                        continue

                    category = Category.objects.filter(category_code=row["category"]).first()
                    if not category:
                        print("Missing Category:", row["category"])
                        skipped += 1
                        continue

                    round_obj = Round.objects.filter(round_code=self.round_code).first()
                    if not round_obj:
                        print("Missing Round:", self.round_code)
                        skipped += 1
                        continue

                    SeatMatrix.objects.update_or_create(
                        college_branch=cb,
                        year=year,
                        category=category,
                        round=round_obj,
                        defaults={
                            "total_seats": int(row["seats"]),
                            "filled_seats": 0
                        }
                    )

                    inserted += 1

            except Exception as e:
                print("❌ Row failed:", e)
                skipped += 1

        print("Inserted:", inserted)
        print("Skipped:", skipped)
