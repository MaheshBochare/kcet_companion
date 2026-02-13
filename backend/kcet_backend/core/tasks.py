from celery import shared_task

import socket

def debug_connection(host, port, name):
    try:
        socket.create_connection((host, port), timeout=5)
        print(f"✅ {name} reachable at {host}:{port}")
    except Exception as e:
        print(f"❌ {name} NOT reachable at {host}:{port} → {e}")


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=30, retry_kwargs={"max_retries": 3})
def scrape_and_ingest_colleges(self):
    """
    Celery task:
    1. Scrape colleges
    2. Match + preprocess
    3. Ingest into DB
    """
    debug_connection("db", 5432, "Postgres")
    debug_connection("redis", 6379, "Redis")

    from core.services.ingestors.college_ingestor import (
        CollegePreprocessor,
        CollegeIngestor,
    )

    processor = CollegePreprocessor(
        scrape_url="https://collegedunia.com/btech/karnataka-colleges?exam_id=61",
        official_excel="/app/core/data/collegedunia_college_names.xlsx",
        sheet_index=3,
    )

    df = processor.run()

    ingestor = CollegeIngestor(df)
    return ingestor.ingest()

