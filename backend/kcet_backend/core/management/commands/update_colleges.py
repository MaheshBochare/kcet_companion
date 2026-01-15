from django.core.management.base import BaseCommand
from core.services.ingestors.college_ingestor import CollegeIngestor

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        CollegeIngestor.run()
        self.stdout.write(self.style.SUCCESS("College ingestion completed"))
