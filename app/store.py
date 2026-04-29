import chromadb
import uuid
from datetime import datetime,timezone

client = chromadb.PersistentClient(path="chroma_db")

def get_collection():
    return client.get_or_create_collection("rag")

def create_document(filename: str) -> str:
    doc_id = f"doc_{uuid.uuid4().hex}"
    get_collection().upsert(
        ids=[doc_id],
        documents=[filename],
        metadatas=[{
            "type": "document",
            "doc_id": doc_id,
            "filename": filename,
            "status": "pending",
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
            "processed_at": "",
            "error_message": ""
        }]
    )
    return doc_id

def update_document_status(doc_id: str, status: str, **kwargs):                                    
      existing = get_collection().get(ids=[doc_id])                                                  
      current_meta = existing["metadatas"][0] if existing["metadatas"] else {}                     
      get_collection().update(
          ids=[doc_id],
          metadatas=[{**current_meta, "status": status, **kwargs}]
      )

def add_page(doc_id: str, page_number: int, row_content: str, key_points: str, filename: str):
    page_id = f"{doc_id}_p{page_number}"
    get_collection().upsert(
        ids=[page_id],
        documents=[row_content],
        metadatas=[{
            "type": "page",
            "doc_id": doc_id,
            "filename": filename,
            "page_number": page_number,
            "key_points": key_points
        }]
    )

def add_chunks(records: list[dict]):
    get_collection().upsert(
        ids=[r["id"] for r in records],
        documents=[r["text"] for r in records],
        metadatas = [r["metadata"] for r in records]
    )

def delete_document(doc_id: str):
    get_collection().delete(where={"doc_id": doc_id})

def list_documents() -> list[dict] | None:
    result = get_collection().get(where={"type": "document"})
    return result["metadatas"] or []

def get_document(doc_id: str) -> dict :
    result = get_collection().get(ids=[doc_id])
    if not result["metadatas"]:
        return {} 
    return result["metadatas"][0]

def list_pages(doc_id: str) -> list[dict] | None:
    result = get_collection().get(where={"$and": [{"type": "page"}, {"doc_id": doc_id}]})
    return result["metadatas"] or []

def get_page(doc_id: str, page_number: int) -> dict | None:
    result = get_collection().get(where={"$and": [{"type": "page"}, {"doc_id": doc_id}, {"page_number": page_number}]})
    if not result["metadatas"]:
        return None
    return result["metadatas"][0]

def search(query: str, n: int = 5) -> list[dict]:
      collection = get_collection()
      total = collection.count()
      if total == 0:
          return []
      result = collection.query(
          query_texts=[query],
          n_results=min(n, total),
          where={"type": "chunk"}
      )
      hits = []
      for i, doc in enumerate(result["documents"][0]):
          meta = result["metadatas"][0][i]
          distance = result["distances"][0][i]
          hits.append({**meta, "text": doc, "distance": distance})
      return hits