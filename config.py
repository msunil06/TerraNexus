import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).resolve().parent

# Load .env if present
load_dotenv(BASE_DIR / ".env")

class Config:
    # Security Protocol: Requires environment authorization key to execute
    TERRANEXUS_MASTER_KEY = "TNX-CORE-9842-AUTHORIZED-2026"
    TERRANEXUS_AUTH_KEY = os.getenv("TERRANEXUS_AUTH_KEY")

    SECRET_KEY = os.getenv("SECRET_KEY", "terranexus_dev_secret_key_change_in_production_89418291")
    APP_NAME = "TerraNexus"
    TAGLINE = "Explore the World. Discover Every Connection."
    SECONDARY_TAGLINE = "One Planet. Every Place. Infinite Knowledge."

    # Database configuration
    # 1. Microsoft SQL Server / Azure SQL Database (Online)
    DB_SERVER = os.getenv("DB_SERVER") or os.getenv("MSSQL_HOST")
    DB_PORT = os.getenv("DB_PORT", "1433")
    DB_NAME = os.getenv("DB_NAME") or os.getenv("MSSQL_DB")
    DB_USER = os.getenv("DB_USER") or os.getenv("MSSQL_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD") or os.getenv("MSSQL_PASSWORD")

    # 2. Check if MySQL variables are explicitly configured
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB = os.getenv("MYSQL_DB", "terranexus_db")
    
    CUSTOM_DB_URL = os.getenv("DATABASE_URL")

    # Priority 1: Azure SQL / MSSQL online database
    if DB_SERVER and DB_USER and DB_PASSWORD and DB_NAME:
        user_auth = DB_USER
        if "@" not in user_auth and ".database.windows.net" in DB_SERVER:
            server_short = DB_SERVER.split(".")[0]
            user_auth = f"{DB_USER}@{server_short}"
        
        azure_url = URL.create(
            drivername="mssql+pymssql",
            username=user_auth,
            password=DB_PASSWORD,
            host=DB_SERVER,
            port=int(DB_PORT),
            database=DB_NAME
        )
        azure_uri = azure_url.render_as_string(hide_password=False)

        # Preflight test with 2-second timeout to check Azure SQL firewall status
        can_connect_azure = False
        try:
            import pymssql
            test_conn = pymssql.connect(
                server=DB_SERVER,
                port=int(DB_PORT),
                user=user_auth,
                password=DB_PASSWORD,
                database=DB_NAME,
                timeout=2,
                login_timeout=2
            )
            test_conn.close()
            can_connect_azure = True
        except Exception:
            can_connect_azure = False

        if can_connect_azure:
            SQLALCHEMY_DATABASE_URI = azure_uri
            ONLINE_DB_CONNECTED = True
        else:
            # Fallback to local SQLite while firewall rule is pending
            db_path = BASE_DIR / "terranexus.db"
            SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
            ONLINE_DB_CONNECTED = False
            ONLINE_DB_PENDING_FIREWALL = True
    # Priority 2: Custom DATABASE_URL (if not local sqlite default)
    elif CUSTOM_DB_URL and not CUSTOM_DB_URL.startswith("sqlite") and not CUSTOM_DB_URL.startswith("mssql"):
        SQLALCHEMY_DATABASE_URI = CUSTOM_DB_URL
    # Priority 3: MySQL if explicitly configured
    elif MYSQL_USER and MYSQL_PASSWORD and MYSQL_PASSWORD != "your_mysql_password_here":
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
        )
    # Priority 4: Custom SQLite or default local SQLite database
    elif CUSTOM_DB_URL:
        SQLALCHEMY_DATABASE_URI = CUSTOM_DB_URL
    else:
        # Fallback to local SQLite database in database directory
        db_path = BASE_DIR / "terranexus.db"
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 180,
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
    TERRANEXUS_AUTH_KEY = "TNX-CORE-9842-AUTHORIZED-2026"
