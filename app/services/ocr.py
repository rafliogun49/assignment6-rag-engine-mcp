from mistralai.client import Mistral
from app.settings import settings

client = Mistral(api_key=settings.MISTRAL_API_KEY)

def extract_pages(pdf_bytes: bytes, filename: str) -> list[tuple[int, str]]:
    uploaded = client.files.upload(
        file={"file_name": filename, "content": pdf_bytes},
        purpose="ocr"
    )    

    signed = client.files.get_signed_url(file_id=uploaded.id)

    response = client.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": signed.url}
    )

    return [(i+1, page.markdown) for i, page in enumerate(response.pages)]