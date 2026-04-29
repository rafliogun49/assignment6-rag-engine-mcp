from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    KEY_POINTS_MODEL: str = os.getenv("KEY_POINTS_MODEL", "")
    KEY_POINTS_API_KEY: str = os.getenv("KEY_POINTS_API_KEY", "")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

settings = Settings()
