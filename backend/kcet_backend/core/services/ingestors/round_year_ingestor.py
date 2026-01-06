from core.models import Round, Year
from django.db import transaction

class RoundYearIngestor:
    def run(self):
        with transaction.atomic():
            for r in ["mock","1gen","2gen","2extgen"]:
                Round.objects.get_or_create(code=r)
            for y in range(2021, 2026):
                Year.objects.get_or_create(year=y)
