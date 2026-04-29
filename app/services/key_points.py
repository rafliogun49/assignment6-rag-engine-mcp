import litellm
from app.settings import settings

def extract_key_points(page_markdown: str) -> str:
    response = litellm.completion(
        model= settings.KEY_POINTS_MODEL,
        api_key=settings.KEY_POINTS_API_KEY,
        messages=[
            {"role": "system", "content": "Extract key facts from the text. Focus on dates, numbers, statistics,names, and organizations. Return as a bullet list."},
            {"role": "user", "content": page_markdown}
        ]
    )
    return response.choices[0].message.content