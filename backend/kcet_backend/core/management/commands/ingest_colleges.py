from django.core.management.base import BaseCommand
from core.services.ingestors.college_ingestor import CollegePreprocessor, CollegeIngestor


class Command(BaseCommand):
    help = "Scrape, match, clean and ingest college data"

    def handle(self, *args, **options):

        self.stdout.write("🔍 Starting college ingestion pipeline...")

        processor = CollegePreprocessor(
            scrape_url="https://collegedunia.com/btech/karnataka-colleges?exam_id=61",
            official_excel=r"C:\Users\mahes\OneDrive\Desktop\kcet_companion\backend\kcet_backend\core\data\collegedunia_college_names.xlsx",
            sheet_index=3
        )

        df = processor.run()

        ingestor = CollegeIngestor(df)
        report = ingestor.ingest()

        self.stdout.write(self.style.SUCCESS(
            f"🎯 Ingestion complete — Created: {report['created']} Updated: {report['updated']} Total: {report['total']}"
        ))
