"""
Application configuration loaded from environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-fallback-secret")
    MONGO_URI = (
        os.environ.get("MONGO_URI", "mongodb://localhost:27017")
        + "/"
        + os.environ.get("MONGO_DB", "gesaivan_market")
    )
    # Pagination
    ITEMS_PER_PAGE = 10
