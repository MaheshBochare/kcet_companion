from core.models import Category
from django.db import transaction

class CategoryIngestor:
    CATEGORIES = ["GM","GMK","GMR","1G","1K","1R","2AG","2AK","2AR","2BG","2BK","2BR",
                  "3AG","3AK","3AR","3BG","3BK","3BR","SCG","SCK","SCR","STG","STK","STR"]

    def run(self):
        
        with transaction.atomic():
            for c in self.CATEGORIES:
                Category.objects.get_or_create(code=c)
