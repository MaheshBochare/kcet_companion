import pandas as pd
import numpy as np
from django.db import transaction

from core.models import College
from core.services.preprocessing.college_pipeline import CollegeScraper
from core.services.preprocessing.college_pipeline import CollegeNameMatcher


# ============================
# Preprocessor
# ============================

class CollegePreprocessor:

    def __init__(self, scrape_url, official_excel, sheet_index):
        self.scrape_url = scrape_url
        self.official_excel = official_excel
        self.sheet_index = sheet_index

    def run(self):
        print("🔍 Scraping colleges...")
        scraper = CollegeScraper(self.scrape_url)
        scraped_df = scraper.scrape()

        print("🧠 Matching official college names...")
        matcher = CollegeNameMatcher(self.official_excel, self.sheet_index)
        matched_df = matcher.match(scraped_df)

        print("🧹 Cleaning & normalizing data...")
        df = matched_df.copy()

        df.replace({np.nan: None}, inplace=True)

        numeric_cols = [
            "First_Year_Fees", "Avg_Package", "Highest_Package",
            "Rating", "National_Ranking"
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df["College_Name"] = df["College_Name"].str.strip()
        df["Location"] = df["Location"].str.strip()

        print(f"✅ Preprocessing complete: {len(df)} clean records")

        return df


# ============================
# Ingestor
# ============================

class CollegeIngestor:

    def __init__(self, df):
        self.df = df

    def _map(self, row):
        return {
            "College_name": row["College_Name"],
            "location": row["Location"],
            "approvals": row["Approvals"],
            "naaccrating": row["NAAC_Grade"],
            "firstyearfees": row["First_Year_Fees"],
            "averagepackage": row["Avg_Package"],
            "highestpackage": row["Highest_Package"],
            "Rating": row["Rating"],
            "nationalrank": row["National_Ranking"]
        }

    @transaction.atomic
    def ingest(self):
        from core.models import College

        # 🛡️ STEP 1: Deduplicate inside the batch
        self.df = self.df.drop_duplicates(subset=["college_code"], keep="last")

        created = updated = skipped = 0

        for _, row in self.df.iterrows():
            data = self._map(row)

            obj, is_created = College.objects.update_or_create(
                college_code=row["college_code"],
                defaults=data
            )

            if is_created:
                created += 1
            else:
                # Detect whether anything actually changed
                changed = any(getattr(obj, k) != v for k, v in data.items())
                if changed:
                    updated += 1
                else:
                    skipped += 1

        print(f"📊 Created: {created} | Updated: {updated} | Skipped: {skipped}")
        return {
            "created": created,
            "updated": updated,
            "skipped": skipped,
            "total": len(self.df)
        }

    def _map(self, row):

        highestpackage = row["Highest_Package"]
        averagepackage = row["Avg_Package"]
        firstyearfees = row["First_Year_Fees"]
        rating = row["Rating"]
        naac = row["NAAC_Grade"]
        nationalrank = row["National_Ranking"]

        # 🔒 IMPUTATION LAYER
        if pd.isna(highestpackage):
            highestpackage = 0

        if pd.isna(averagepackage):
            averagepackage = 0

        if pd.isna(firstyearfees):
            firstyearfees = 450000

        if pd.isna(rating):
            rating = 3.5
        if pd.isna(nationalrank):
            nationalrank = None

        if not naac or pd.isna(naac):
            naac = "No NAAC"

        return {
            "College_name": row["College_Name"],
            "location": row["Location"],
            "approvals": row["Approvals"],
            "naaccrating": naac,
            "firstyearfees": firstyearfees,
            "averagepackage": averagepackage,
            "highestpackage": highestpackage,
            "Rating": rating,
            "nationalrank": nationalrank
        }
