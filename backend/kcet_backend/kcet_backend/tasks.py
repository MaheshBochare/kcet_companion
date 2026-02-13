from celery import shared_task
from core.services.ingestors.college_ingestor import (
    CollegePreprocessor,
    CollegeIngestor,
)

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def scrape_and_ingest_colleges(self):
    self.update_state(state="PROGRESS", meta={"step": "scraping"})

    preprocessor = CollegePreprocessor(
        scrape_url="https://collegedunia.com/btech/karnataka-colleges?exam_id=61",
        official_excel="/app/core/data/collegedunia_college_names.xlsx",
        sheet_index=3,
    )

    df = preprocessor.run()

    self.update_state(state="PROGRESS", meta={"step": "ingesting"})

    ingestor = CollegeIngestor(df)
    result = ingestor.ingest()

    return {
        "status": "completed",
        "stats": result,
    }
