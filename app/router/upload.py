from fastapi import APIRouter, UploadFile, File, HTTPException
from app import store
from app.tasks import process_upload
import os, uuid

router = APIRouter()

@router.post("/upload/")
async def upload(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    os.makedirs("data/uploads", exist_ok=True)
    file_path = f"data/uploads/{uuid.uuid4().hex}.pdf"
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    
    doc_id = store.create_document(file.filename or "unknown.pdf")
    process_upload.delay(doc_id, file_path)

    return store.get_document(doc_id)
