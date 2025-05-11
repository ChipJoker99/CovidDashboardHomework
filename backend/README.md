# COVID-19 Data API - Backend

This directory contains the Python FastAPI backend for the COVID-19 Italy Data Dashboard. Its primary role is to serve processed and aggregated epidemiological data to the frontend client.

## Responsibilities

*   **Data Ingestion:** Fetches raw provincial data (JSON for latest, CSV for historical) from the DPC's GitHub repository.
*   **Data Processing:** Validates, cleans, and aggregates provincial case data to calculate regional totals. Converts data types as needed.
*   **Data Persistence:** Stores processed regional data in a local SQLite database using SQLAlchemy ORM, with Alembic managing schema migrations. Implements an "upsert" logic to avoid data duplication for a given date and region.
*   **API Exposure:** Provides RESTful API endpoints for the frontend to retrieve regional data, supporting date-specific queries and dynamic sorting.
*   **Error Handling:** Implements error handling for data fetching, processing, and database operations, returning appropriate HTTP status codes.
*   **(Planned) Data Export:** Will provide an endpoint to export data in `.xlsx` format.

## Tech Stack

*   Python 3.10+
*   FastAPI & Uvicorn (ASGI server)
*   SQLAlchemy (ORM) & Alembic (Database Migrations)
*   SQLite (Database)
*   `httpx` (Asynchronous HTTP Client)
*   `openpyxl` (For Excel generation - planned)
*   Pydantic (Data validation and serialization)
*   `python-dotenv` (Environment variable management)

## Project Structure (within `backend/app/`)

*   `main.py`: FastAPI application entry point, global middleware (CORS, central logging configuration), and API router inclusion.
*   `core/`: Application settings (`config.py` for database URLs, external source URLs, etc.).
*   `db/`: Database session management (`session.py`), base SQLAlchemy model.
*   `data/`: Contains the `covid_data.db` SQLite file (auto-created by Alembic or on first app run if directory doesn't exist).
*   `models/`: SQLAlchemy ORM model definitions (e.g., `region_data.py` defining the `RegionalCovidData` table).
*   `schemas/`: Pydantic schemas for data validation and API request/response serialization (e.g., `region_data_schema.py`).
*   `services/`: Core business logic modules:
    *   `data_fetcher.py`: Responsible for fetching raw data (JSON/CSV) from the DPC GitHub source. Handles network errors and source-specific data quirks.
    *   `data_processor.py`: Takes raw data from the fetcher, cleans it, converts types (e.g., string dates to date objects, case numbers to integers), and aggregates provincial data into regional totals.
*   `crud/`: Data Access Layer (DAL) functions.
    *   `crud_region_data.py`: Contains functions for Create, Read, Update, Delete (CRUD) operations on the `RegionalCovidData` table (e.g., fetching by date, bulk create/update).
*   `api/`: FastAPI router definitions.
    *   `api_v1/endpoints/`: Contains modules for specific groups of endpoints.
        *   `regions.py`: Defines endpoints related to regional COVID-19 data retrieval (e.g., `GET /api/v1/regions/`).
        *   *(export.py: To be added for XLSX export functionality)*

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
    *   Copy the example environment file if it doesn't exist:
        ```bash
        cp .env.example .env
        ```
    *   Review `backend/.env`. The default `DATABASE_URL` in `app/core/config.py` points to a local SQLite file (`./app/data/covid_data.db`) and should work out-of-the-box. The `DPC_REPO_BASE_URL` also has a sensible default.

5.  **Database Migrations (Alembic):**
    *   The SQLite database file will be created in `backend/app/data/covid_data.db`. The `app/core/config.py` script ensures the `backend/app/data/` directory is created if missing.
    *   **To apply migrations and create database tables:**
        ```bash
        alembic upgrade head
        ```
    *   **If you modify SQLAlchemy models** (in `app/models/`):
        1.  Generate a new migration script:
            ```bash
            alembic revision -m "short_description_of_model_changes" --autogenerate
            ```
        2.  Review the generated script in `alembic/versions/`.
        3.  Apply the migration:
            ```bash
            alembic upgrade head
            ```

## Running the Backend Server

1.  Ensure your Python virtual environment (`venv`) is activated.
2.  From the `backend` directory, execute:
    ```bash
    uvicorn app.main:app --reload
    ```
    *   The `--reload` flag enables auto-reloading on code changes, which is beneficial during development.
3.  The API will typically be accessible at `http://127.0.0.1:8000`.
4.  Interactive API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.
5.  Alternative API documentation (ReDoc) is at `http://127.0.0.1:8000/redoc`.

## API Endpoints Implemented

*   **`GET /api/v1/regions/`**
    *   **Description:** Retrieves COVID-19 data aggregated by Italian region.
    *   **Query Parameters:**
        *   `report_date` (string, optional, format: `YYYY-MM-DD`): Fetches data for this specific date. Defaults to the latest available data if omitted.
        *   `sort_by` (string, optional): Field to sort by (e.g., `total_positive_cases`, `region_name`).
        *   `sort_order` (string, optional, `asc` or `desc`): Sorting direction.
    *   **Functionality:** If data for the requested date (or latest) isn't in the local DB, it's fetched from the DPC source, processed, stored, and then returned. Subsequent requests for the same date are served from the DB. Default sort order is by total cases (desc) then region name (asc).

## Troubleshooting / Maintenance

*   **`sqlite3.OperationalError: unable to open database file` (Alembic):** Ensure the `backend/app/data/` directory exists and is writable. The `sqlalchemy.url` in `alembic.ini` should be `sqlite:///./app/data/covid_data.db` (relative to `backend/`).
*   **Data Fetching Issues (404s, etc.):**
    *   Verify the URLs in `app/core/config.py` (`DPC_REPO_BASE_URL`, etc.) are correct and the DPC repository structure hasn't changed.
    *   Check network connectivity.
    *   Examine logs from `uvicorn` for detailed error messages from `data_fetcher.py`.
*   **Data Processing Issues:** Check `data_processor.py` logs for errors related to data parsing or aggregation. Ensure source data format (JSON/CSV fields) matches expectations.
*   **CORS Errors from Frontend:** Ensure `app.main.py` has `CORSMiddleware` configured correctly, and the frontend's origin (e.g., `http://localhost:5173`) is in the `allow_origins` list.