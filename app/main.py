from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.router import upload, documents, search

app = FastAPI(title="RAG API")

app.include_router(upload.router)
app.include_router(documents.router)
app.include_router(search.router)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/scalar", include_in_schema=False)
def scalar_html():
    return get_scalar_api_reference(
    openapi_url= app.openapi_url,
    title="RAG API"
    )