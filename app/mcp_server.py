from fastmcp import FastMCP
from app import store

mcp = FastMCP("rag-engine")

@mcp.tool()
def search(query: str, n: int = 5) -> list[dict]:
    """
    Use this to semantically search the knowledge base.
    Returns top-N chunks with doc_id, filename, page_number, distance.
    Call this FIRST when the user asks about indexed documents.
    """
    return store.search(query, n) or []

@mcp.tool()
def get_page(doc_id: str, page_number: int) -> dict:
    """
    Use this to fetch the full text of a specific page.
    Call this AFTER search when a chunk's context is insufficient
    and you need the surrounding page content.
    """
    return store.get_page(doc_id, page_number) or {}

if __name__ == "__main__":
    mcp.run()