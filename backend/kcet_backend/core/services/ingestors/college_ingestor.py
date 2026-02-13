import pandas as pd
import numpy as np
from django.db import transaction


# ============================
# Preprocessor (SAFE)
# ============================

class CollegePreprocessor:
    """
    Responsible ONLY for:
    - Scraping
    - Matching
    - Cleaning
    """

    def __init__(self, scrape_url, official_excel, sheet_index):
        self.scrape_url = scrape_url
        self.official_excel = official_excel
        self.sheet_index = sheet_index

    def run(self):
        print("🔍 Scraping colleges...")

        # 🔒 Lazy imports (critical for stability)
        from core.services.preprocessing.college_pipeline import (
            CollegeScraper,
            CollegeNameMatcher,
        )

        scraper = CollegeScraper(self.scrape_url)
        scraped_df = scraper.scrape()

        print("🧠 Matching official college names...")
        matcher = CollegeNameMatcher(self.official_excel, self.sheet_index)
        matched_df = matcher.match(scraped_df)

        print("🧹 Cleaning & normalizing data...")
        df = matched_df.copy()

        df.replace({np.nan: None}, inplace=True)

        numeric_cols = [
            "First_Year_Fees",
            "Avg_Package",
            "Highest_Package",
            "Rating",
            "National_Ranking",
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df["College_Name"] = df["College_Name"].str.strip()
        df["Location"] = df["Location"].str.strip()

        print(f"✅ Preprocessing complete: {len(df)} clean records")
        return df


# ============================
# Ingestor (SAFE)
# ============================

class CollegeIngestor:
    """
    Responsible ONLY for:
    - Imputation
    - Validation
    - Saving to DB
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    # ------------------------
    # Imputation + Mapping
    # ------------------------
    def _map_row(self, row):
        def _num(val, default):
            return default if pd.isna(val) else val

        return {
            "College_name": row["College_Name"],
            "location": row["Location"],
            "approvals": row["Approvals"],
            "naaccrating": row["NAAC_Grade"] or "No NAAC",
            "firstyearfees": _num(row["First_Year_Fees"], 450000),
            "averagepackage": _num(row["Avg_Package"], 0),
            "highestpackage": _num(row["Highest_Package"], 0),
            "Rating": _num(row["Rating"], 3.5),
            "nationalrank": row["National_Ranking"],
        }

    # ------------------------
    # DB Ingestion
    # ------------------------
    @transaction.atomic
    def ingest(self):
        from core.models import College  # lazy import

        self.df = self.df.drop_duplicates(
            subset=["college_code"], keep="last"
        )

        created = updated = skipped = 0

        for _, row in self.df.iterrows():
            data = self._map_row(row)

            existing = College.objects.filter(
                college_code=row["college_code"]
            ).first()

            if existing:
                changed = any(
                    getattr(existing, k) != v for k, v in data.items()
                )
                if changed:
                    for k, v in data.items():
                        setattr(existing, k, v)
                    existing.save()
                    updated += 1
                else:
                    skipped += 1
            else:
                College.objects.create(
                    college_code=row["college_code"],
                    **data
                )
                created += 1

        print(
            f"📊 Created: {created} | "
            f"Updated: {updated} | "
            f"Skipped: {skipped}"
        )

        return {
            "created": created,
            "updated": updated,
            "skipped": skipped,
            "total": len(self.df),
        }
