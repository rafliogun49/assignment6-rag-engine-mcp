from fastapi import APIRouter, HTTPException
from app import store

router = APIRouter()

@router.get("/documents/")
def list_documents():
    return store.list_documents()

@router.get("/documents/{doc_id}")
def get_documents(doc_id: str):
    doc = store.get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    pages = store.list_pages(doc_id)
    return {"document": doc, "pages": pages}

@router.get("/documents/{doc_id}/pages/{page_number}")
def get_page(doc_id: str, page_number: int):
    page = store.get_page(doc_id, page_number)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page