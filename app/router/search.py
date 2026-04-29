from fastapi import APIRouter
from app import store

router = APIRouter()

@router.get("/search/")
def search(q: str, n: int = 5):
    return store.search(q,n)