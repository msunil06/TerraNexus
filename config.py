import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load .env if present
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "terranexus_dev_secret_key_change_in_production_89418291")
    APP_NAME = "TerraNexus"
    TAGLINE = "Explore the World. Discover Every Connection."
    SECONDARY_TAGLINE = "One Planet. Every Place. Infinite Knowledge."

    # Database configuration
    # Check if MySQL variables are explicitly configured
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB = os.getenv("MYSQL_DB", "terranexus_db")
    
    CUSTOM_DB_URL = os.getenv("DATABASE_URL")

    if CUSTOM_DB_URL:
        SQLALCHEMY_DATABASE_URI = CUSTOM_DB_URL
    elif MYSQL_USER and MYSQL_PASSWORD and MYSQL_PASSWORD != "your_mysql_password_here":
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
        )
    else:
        # Fallback to local SQLite database in database directory
        db_path = BASE_DIR / "terranexus.db"
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 280,
        "pool_pre_ping": True,
    }

    # Session & Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False").lower() in ("true", "1")
    PERMANENT_SESSION_LIFETIME = 86400 * 7 # 7 days
    WTF_CSRF_ENABLED = True

    # Pagination
    ITEMS_PER_PAGE = 24
    SEARCH_RESULTS_LIMIT = 20

    # Geo Data Paths
    DATA_DIR = BASE_DIR / "static" / "data"

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "test-secret-key"
