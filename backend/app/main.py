from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
from app.core.config import settings
from app.api.api_v1.endpoints import regions_router, export_router

# --- Logging Configuration---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend_app.log"),
    ]
)
logger = logging.getLogger(__name__)


# --- FastAPI app Instances ---
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"/api/v1/openapi.json"
)

# --- Middleware ---
origins = [
    "http://localhost",         # React (Create React App default)
    "http://localhost:3000",    # React (Create React App default)
    "http://localhost:5173",    # Vite (React/Vue default)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- API ROUTERs ---
app.include_router(regions_router, prefix="/api/v1/regions", tags=["Regions"])
app.include_router(export_router, prefix="/api/v1/export", tags=["Export"])


# --- Root Endpoints ---
@app.get("/", tags=["Root"])
async def read_root():
    logger.info("Root endpoint was called.")
    return {"message": f"Welcome to the {settings.PROJECT_NAME}!"}


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown...")

# Per avviare Uvicorn da terminale (dalla cartella 'backend/'):
# uvicorn app.main:app --reload