from app.celery_app import celery
from datetime import datetime, timezone
from app import store
from app.services.ocr import extract_pages
from app.services.key_points import extract_key_points
from app.services.chunker import chunk_for_indexing

@celery.task
def process_upload(doc_id: str, file_path: str):
    try:
        store.update_document_status(doc_id, "processing")
        doc = store.get_document(doc_id)
        filename = doc["filename"]
        
        with open(file_path, "rb") as f:
            pdf_bytes = f.read()

        pages = extract_pages(pdf_bytes, filename)

        pages_with_kp = []
        for page_number, markdown in pages:
            key_points = extract_key_points(markdown)
            store.add_page(doc_id, page_number, markdown, key_points, filename)
            pages_with_kp.append((page_number, key_points))

        records = chunk_for_indexing(doc_id, filename,pages_with_kp)
        store.add_chunks(records)

        store.update_document_status(doc_id, "done", processed_at=datetime.now(timezone.utc).isoformat())

    except Exception as e:
        store.update_document_status(doc_id, "failed", error_message=str(e))