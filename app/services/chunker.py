from chonkie import SemanticChunker

chunker = SemanticChunker(chunk_size=512, threshold=0.5)

def chunk_for_indexing(doc_id: str, filename: str, pages_with_kp: list[tuple[int, str]]) -> list[dict]:
    records = []
    for page_number, key_points in pages_with_kp:
        chunks = chunker.chunk(key_points)
        for i, chunk in enumerate(chunks):
            records.append({
                "id": f"{doc_id}_p{page_number}_c{i}",
                "text": chunk.text,
                "metadata": {
                    "type": "chunk",
                    "doc_id": doc_id,
                    "filename": filename,
                    "page_number": page_number,
                    "chunk_idx": i
                }
            }
            )
    return records