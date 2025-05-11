# COVID-19 Data API - Backend

This directory contains the Python FastAPI backend for the COVID-19 Italy Data Dashboard.

## Responsibilities

*   Fetching data from the Civil Protection Department's GitHub repository.
*   Processing and aggregating provincial data into regional totals.
*   Storing and retrieving data from an SQLite database.
*   Exposing a RESTful API for the frontend to consume.
*   Handling data export декоративно.xlsx format.

## Tech Stack

*   Python 3.10+
*   FastAPI & Uvicorn
*   SQLAlchemy & Alembic (for SQLite)
*   `httpx` for asynchronous HTTP requests
*   `openpyxl` for Excel generation
*   `python-dotenv` for environment variable management

## Project Structure (within `backend/app/`)

*   `main.py`: FastAPI application entry point, global middleware.
*   `core/`: Application settings, configuration (`config.py`).
*   `db/`: Database session management (`session.py`), base model.
*   `data/`: Contains the `covid_data.db` SQLite file (auto-created).
*   `models/`: SQLAlchemy ORM models (e.g., `region_data.py`).
*   `schemas/`: Pydantic schemas for data validation and serialization in API requests/responses.
*   `services/`: Business logic modules:
    *   `data_fetcher.py`: Fetches raw data from the external source.
    *   `data_processor.py`: Processes and aggregates raw data.
    *   `db_service.py` (or `crud.py`): Handles database create, read, update, delete operations.
*   `api/`: FastAPI routers defining API endpoints.
    *   `api_v1/`: Version 1 of the API.
        *   `endpoints/`: Specific endpoint modules (e.g., `regions.py`, `export.py`).

## Setup

1.  **Navigate to the `backend` directory:**
    ```bash
    cd path/to/your/project/COVID-DASHBOARD/backend
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables:**
    *   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    *   Review and modify `backend/.env` if necessary. Defaults are generally sufficient for local development with SQLite.

5.  **Database Migrations:**
    *   The SQLite database file will be created in `backend/app/data/covid_data.db`.
    *   The `backend/app/core/config.py` script will attempt to create the `backend/app/data/` directory if it doesn't exist when the app starts or when Alembic needs it.
    *   To apply migrations (create tables):
        ```bash
        alembic upgrade head
        ```
    *   If you make changes to SQLAlchemy models in `app/models/`, you'll need to generate a new migration:
        ```bash
        alembic revision -m "describe_your_change" --autogenerate
        alembic upgrade head
        ```

## Running the Backend Server

1.  Ensure your virtual environment is activated.
2.  From the `backend` directory, run:
    ```bash
    uvicorn app.main:app --reload
    ```
    *   `--reload` enables auto-reloading when code changes, useful for development.
3.  The API will be available at `http://127.0.0.1:8000`.
4.  Interactive API documentation (Swagger UI) can be accessed at `http://127.0.0.1:8000/docs`.
5.  Alternative API documentation (ReDoc) can be accessed at `http://127.0.0.1:8000/redoc`.

## Running Tests (if implemented)

```bash
# pytest # (Example command if using pytest)