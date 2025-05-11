import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    # FALLBACK IF .ENV IN PROJECT ROOT
    dotenv_path_project_root = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
    if os.path.exists(dotenv_path_project_root):
        load_dotenv(dotenv_path=dotenv_path_project_root)

class Settings:
    PROJECT_NAME: str = "COVID-19 Data API"
    PROJECT_VERSION: str = "0.1.0"

    BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_DIR = os.path.join(BACKEND_DIR, "data")
    
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR, exist_ok=True)
    
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(DATABASE_DIR, 'covid_data.db')}")

    # --- DATA SOURCE ---
    DPC_REPO_BASE_URL: str = os.getenv("DPC_REPO_BASE_URL", "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/")
    PROVINCES_LATEST_FILENAME: str = "dpc-covid19-ita-province-latest.json"
    PROVINCES_DATE_FILENAME_FORMAT: str = "dpc-covid19-ita-province-{date_str}.json" # YYYYMMDD

settings = Settings()

# DEBUGGING TO VERIFY PATHS
# print(f"BACKEND_DIR: {Settings.BACKEND_DIR}")
# print(f"DATABASE_DIR: {Settings.DATABASE_DIR}")
# print(f"SQLALCHEMY_DATABASE_URL: {settings.SQLALCHEMY_DATABASE_URL}")