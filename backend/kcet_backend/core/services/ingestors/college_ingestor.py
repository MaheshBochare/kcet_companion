from core.services.preprocessing.college_scraper import CollegeIngestionService


class CollegeScrapeIngestor:
    """
    One-click college refresh:
    Scrape → Match → Clean → Insert into DB
    """

    def run(self):
        print("\n🚀 Starting College Scrape + Ingestion Pipeline...\n")

        count = CollegeIngestionService.refresh_colleges()

        print(f"\n✅ College Ingestion Completed Successfully: {count} records updated\n")
        return count
