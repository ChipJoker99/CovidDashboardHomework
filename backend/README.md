# COVID-19 Data API - Backend

This directory contains the Python FastAPI backend for the COVID-19 Italy Data Dashboard. It serves as the data engine, responsible for acquisition, processing, storage, and exposure of epidemiological data through a well-defined API.

## Core Responsibilities & Design Philosophy

The backend is architected with several key principles in mind:

* **Reliable Data Acquisition:** Robustly fetch data from the DPC's GitHub, handling potential inconsistencies in source data (e.g., JSON for latest, CSV for historical) and network unreliability.
* **Efficient Data Processing:** Transform raw provincial data into meaningful, aggregated regional insights with necessary type conversions and validations.
* **Optimized Data Persistence:** Utilize a local SQLite database as an intelligent cache, minimizing redundant external fetches and ensuring swift API responses for previously accessed data. Alembic ensures schema integrity and evolution.
* **Clean API Design:** Expose data via a RESTful API built with FastAPI, leveraging Pydantic for request/response validation and serialization, and providing auto-generated documentation.
* **Asynchronous First:** All I/O-bound operations are asynchronous to maximize performance and scalability under load.

## Tech Stack & Rationale

* **Python 3.10+ & FastAPI:** Chosen for its high performance, asynchronous capabilities ideal for I/O tasks, and developer-friendly features like Pydantic integration for automatic validation and OpenAPI schema generation.
* **SQLAlchemy & Alembic:** SQLAlchemy provides a powerful ORM for flexible database interaction, while Alembic offers robust schema migration management, crucial for maintaining database integrity over time.
* **SQLite:** Selected for its simplicity and serverless nature, ideal for this project's scale and ease of deployment/evaluation. It serves as an effective local cache.
* **`httpx`:** A modern async HTTP client, aligning with FastAPI's async-first approach for efficient external data fetching.
* **Pydantic:** Integral to FastAPI, used for rigorous data validation at API boundaries and for defining clear data schemas, enhancing API reliability.
* **`openpyxl`:** Standard library for XLSX file generation, directly addressing the export requirement.

## Project Structure (`backend/app/`)

* `main.py`: FastAPI application entry point, global middleware (CORS, central logging configuration), and API router inclusion.
* `core/`: Application settings (`config.py` for database URLs, external source URLs, etc.).
* `db/`: Database session management (`session.py`), base SQLAlchemy model.
* `data/`: Contains the `covid_data.db` SQLite file (auto-created by Alembic or on first app run if directory doesn't exist).
* `models/`: SQLAlchemy ORM model definitions (e.g., `region_data.py` defining the `RegionalCovidData` table).
* `schemas/`: Pydantic schemas for data validation and API request/response serialization (e.g., `region_data_schema.py`).
* `services/`:
  * `data_fetcher.py`: Encapsulates all logic for retrieving data from the DPC. It handles different file formats (JSON/CSV) and source URLs, abstracting these details from the rest of the application. Implements retries or specific error handling for source unavailability.
  * `data_processor.py`: Responsible for transforming raw data (list of provincial records) into aggregated regional data. This includes type casting (e.g., string to int/date), validation of essential fields, and summing `totale_casi` per region.
* `crud/crud_region_data.py`: Implements the Data Access Layer (DAL). Contains all SQLAlchemy queries and database transaction logic (create, read, upsert) for `RegionalCovidData`. This separation ensures that database interaction logic is not scattered throughout the application.
* `api/`: FastAPI router definitions.
  * `api_v1/endpoints/`: Contains modules for specific groups of endpoints.
    * `regions.py`: Defines the `/regions/` endpoint. Orchestrates calls to `ensure_data_is_available` (which internally uses fetcher, processor, and CRUD) and then to CRUD functions for final data retrieval and sorting.
    * `export.py`: Defines the `/export/regions.xlsx` endpoint. Retrieves data (via CRUD) based on query parameters and uses `openpyxl` to generate and stream the XLSX file.

## Setup

1. **Navigate to the `backend` directory:**

   ```bash
   cd path/to/your/project/COVID-DASHBOARD/backend
   ```
2. **Create and activate a Python virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables:**

   * Copy the example environment file if it doesn't exist:
     ```bash
     cp .env.example .env
     ```
   * Review `backend/.env`. The default `DATABASE_URL` in `app/core/config.py` points to a local SQLite file (`./app/data/covid_data.db`) and should work out-of-the-box. The `DPC_REPO_BASE_URL` also has a sensible default.
5. **Database Migrations (Alembic):**

   * The SQLite database file will be created in `backend/app/data/covid_data.db`. The `app/core/config.py` script ensures the `backend/app/data/` directory is created if missing.
   * **To apply migrations and create database tables:**
     ```bash
     alembic upgrade head
     ```
   * **If you modify SQLAlchemy models** (in `app/models/`):
     1. Generate a new migration script:
        ```bash
        alembic revision -m "short_description_of_model_changes" --autogenerate
        ```
     2. Review the generated script in `alembic/versions/`.
     3. Apply the migration:
        ```bash
        alembic upgrade head
        ```

## Running the Backend Server

1. Ensure your Python virtual environment (`venv`) is activated.
2. From the `backend` directory, execute:

   ```bash
   uvicorn app.main:app --reload
   ```

   * The `--reload` flag enables auto-reloading on code changes, which is beneficial during development.
3. The API will typically be accessible at `http://127.0.0.1:8000`.
4. Interactive API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.
5. Alternative API documentation (ReDoc) is at `http://127.0.0.1:8000/redoc`.

## API Endpoints Implemented

The API is versioned under `/api/v1/`.

### 1. Regional Data Retrieval

* **Endpoint:** `GET /api/v1/regions/`
* **HTTP Method:** `GET`
* **Description:** Retrieves COVID-19 case data aggregated by Italian region. This endpoint implements a "fetch-on-demand" and "cache-locally" strategy.
* **Query Parameters:**

  * `report_date` (string, optional, format: `YYYY-MM-DD`):
    * If provided, the endpoint attempts to retrieve data for this specific date.
    * If omitted, the endpoint defaults to fetching data for the current calendar day (`date.today()`).
  * `sort_by` (string, optional): Field to sort the results by. Supported values: `total_positive_cases`, `region_name`.
  * `sort_order` (string, optional, enum: `asc`, `desc`): The order of sorting. Default behavior depends on `sort_by`.
* **Response (Success - 200 OK):** A JSON array of regional data objects, each containing:

  * `id` (integer): Database ID.
  * `submission_date` (string, `YYYY-MM-DD`): The actual date of the data report.
  * `region_code` (string): Unique code for the region.
  * `region_name` (string): Name of the region.
  * `total_positive_cases` (integer): Aggregated total cases for the region on that date.
* **Response (Error):**

  * `404 Not Found`: If data for the requested `report_date` (or latest, if `report_date` was omitted) cannot be found either in the local database or from the external DPC source.
  * `500 Internal Server Error`: If there's an issue during data processing or an unexpected server error.
  * `502 Bad Gateway`: If fetching data from the external DPC source fails due to network issues or source unavailability.
* **Detailed Behavior & Data Flow:**

  1. **Determine Target Date:**
     * If `report_date` query parameter is provided, it's used as the `target_date`.
     * If `report_date` is omitted, `target_date` is set to the current calendar day (`date.today()`).
  2. **Check Local Database (Cache):**
     * The system first checks if data for the `target_date` already exists in the local SQLite database (function `crud_regional_data.data_exists_for_date`).
  3. **Fetch from External Source (if necessary):**
     * **If data for `target_date` is NOT in the local DB:**
       * If `target_date` was today: The system attempts to fetch the `dpc-covid19-ita-province-latest.json` file from the DPC GitHub repository.
       * If `target_date` was a specific past date: The system attempts to fetch the corresponding `dpc-covid19-ita-province-YYYYMMDD.csv` file.
       * If fetching fails (e.g., DPC source returns 404 for that date, or network error), an appropriate HTTP error (404 or 502) is returned to the client.
     * **Data Processing:** If raw data is successfully fetched, it's processed:
       * Provincial data is aggregated to regional totals.
       * Data types are normalized (e.g., case counts to integers, date strings to date objects).
       * The actual report date (`actual_report_date`) is determined from the content of the fetched file (this is important because "latest.json" might contain data for yesterday if today's file isn't published yet).
     * **Store in Local Database:**
       * The processed regional data is saved to the local SQLite database, associated with its `actual_report_date`. An "upsert" logic is used: if data for that `actual_report_date` and region already exists, it's updated; otherwise, a new record is created. This prevents data duplication and ensures the DB reflects the fetched content.
       * This step is skipped if data for `actual_report_date` was already present (e.g. 'latest' was for yesterday, and yesterday's data was already in DB).
  4. **Retrieve from Local Database for Response:**
     * After the above steps (data either existed, or was fetched and stored), the system queries the local database for records matching the `target_date`.
     * **Handling "Today" vs. "Latest":** If the initial `target_date` was today, but no records were found for today (e.g., because the DPC "latest" file was for yesterday and today's data hasn't been processed/saved yet), the system attempts to retrieve records for the most recent `submission_date` available in the database.
     * The retrieved records are then sorted according to `sort_by` and `sort_order` parameters. The default sorting (if no parameters are provided) is by `total_positive_cases` (descending) and then `region_name` (ascending).
  5. **Return Response:** The sorted list of regional data (as Pydantic models serialized to JSON) is returned to the client. If no data can be ultimately found for the query, a 404 is returned.

### 2. Regional Data Export to XLSX

* **Endpoint:** `GET /api/v1/export/regions.xlsx`
* **HTTP Method:** `GET`
* **Description:** Exports regional COVID-19 data to an XLSX (Excel) file. This endpoint works with data **already present** in the local database.
* **Query Parameters:**

  * `report_date` (string, optional, format: `YYYY-MM-DD`):
    * If provided, the endpoint attempts to export data for this specific date from the local database.
    * If omitted, the endpoint defaults to exporting data for the most recent `submission_date` found in the local database.
  * `sort_by` (string, optional): Field to sort the data by within the Excel file (e.g., `total_positive_cases`, `region_name`).
  * `sort_order` (string, optional, enum: `asc`, `desc`): Sorting direction.
* **Response (Success - 200 OK):**

  * An XLSX file download is triggered in the client's browser.
  * **Headers:**
    * `Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
    * `Content-Disposition: attachment; filename="covid_data_regioni_YYYYMMDD.xlsx"` (filename includes the relevant date).
  * **Content:** The Excel file contains a single sheet with columns: "Regione", "Totale Casi Positivi", "Data Riferimento". Data is sorted as per query parameters.
* **Response (Error):**

  * `404 Not Found`: If no data exists in the local database for the specified `report_date` (or for the latest date if `report_date` was omitted). This endpoint **does not** attempt to fetch data from the external DPC source if it's missing locally.
* **Detailed Behavior & Data Flow:**

  1. **Determine Target Date for Export:**
     * If `report_date` query parameter is provided, it's used as the `target_date_to_query`. The system first checks if any data exists in the local database for this `target_date_to_query`. If not, a 404 error is returned immediately.
     * If `report_date` is omitted, the system queries the local database for the most recent `submission_date` for which data exists. If the database is empty, a 404 error is returned. This most recent date becomes the `target_date_to_query`.
  2. **Retrieve Data from Local Database:**
     * The system queries the local SQLite database for all regional records matching the `target_date_to_query`.
     * The retrieved records are sorted according to the `sort_by` and `sort_order` query parameters. The default sorting matches that of the `/regions/` endpoint.
     * If, for any reason, no records are found for the `target_date_to_query` at this stage (e.g., an unlikely race condition or data inconsistency), a 404 error is returned.
  3. **Generate XLSX File:**
     * An Excel workbook is created in memory using the `openpyxl` library.
     * A sheet is added, named with the `target_date_to_query`.
     * Headers ("Regione", "Totale Casi Positivi", "Data Riferimento") are written.
     * The sorted regional data records are written row by row into the sheet.
     * Column widths are auto-adjusted for better readability.
  4. **Return File Stream:**
     * The generated Excel workbook is saved to an in-memory byte buffer (`io.BytesIO`).
     * A `StreamingResponse` is used to send this buffer to the client, with appropriate `Content-Type` and `Content-Disposition` headers to trigger a file download.

### 3. Root Endpoint

* **Endpoint:** `GET /`
* **Description:** A simple root endpoint, primarily for a basic health check or welcome message.
* **Response:** A JSON object: `{"message": "Welcome to the COVID-19 Data API!"}`

## Key Technical Decisions & Implementation Details

* **Data Caching Strategy:** The primary mechanism for performance is caching processed data in the SQLite DB. The `/regions/` endpoint checks the DB first. If data for a specific date (especially historical) is present, it's served directly. If not, it's fetched, processed, stored, then served. This significantly reduces latency on subsequent requests and load on the DPC server.
* **"Upsert" Logic for Data Integrity:** When storing data, `crud_region_data.create_or_update_bulk` checks if a record for a given region and date already exists. If so, it updates it; otherwise, it creates a new one. This prevents duplicates and ensures data consistency if, hypothetically, source data for a past date were to be re-fetched and re-processed.
* **Asynchronous Operations:** The use of `async def` throughout the FastAPI request lifecycle, along with `httpx` for external calls, ensures that the application remains responsive and doesn't block while waiting for I/O.
* **Centralized Configuration:** `app/core/config.py` (potentially loading from `.env` files) centralizes settings like database URLs and external API endpoints, making the application easier to configure for different environments.
* **Dependency Injection (FastAPI Depends):** `Depends(get_db)` is used to manage database sessions per request, ensuring sessions are properly created and closed, which is crucial for resource management and preventing connection leaks.
* **Error Handling Strategy:** Custom exceptions (e.g., `DataFetchingError`, `DataProcessingError`) are used in services, and API endpoints translate these into appropriate HTTPExceptions with user-friendly (or at least API-client-friendly) error messages and status codes. This provides clear feedback to the client in case of issues.

## Troubleshooting & Maintenance

* **`sqlite3.OperationalError: unable to open database file` (Alembic):** Ensure the `backend/app/data/` directory exists and is writable. The `sqlalchemy.url` in `alembic.ini` should be `sqlite:///./app/data/covid_data.db` (relative to `backend/`).
* **Data Fetching Issues (404s, etc.):**
  * Verify the URLs in `app/core/config.py` (`DPC_REPO_BASE_URL`, etc.) are correct and the DPC repository structure hasn't changed.
  * Check network connectivity.
  * Examine logs from `uvicorn` for detailed error messages from `data_fetcher.py`.
* **Data Processing Issues:** Check `data_processor.py` logs for errors related to data parsing or aggregation. Ensure source data format (JSON/CSV fields) matches expectations.
* **CORS Errors from Frontend:** Ensure `app.main.py` has `CORSMiddleware` configured correctly, and the frontend's origin (e.g., `http://localhost:5173`) is in the `allow_origins` list.
* **"Latest" Data Discrepancy:** If the data for "today" appears to be from yesterday, it's likely because the DPC's `latest.json` file has not yet been updated for the current calendar day. The application will fetch and store the data corresponding to the `data` field within that `latest.json` file.
* **Alembic Migrations:** Always run `alembic revision --autogenerate` and `alembic upgrade head` after changing SQLAlchemy models to keep the database schema in sync with your models.
* **SQLite File Location:** The database `covid_data.db` is created within `backend/app/data/`. If you move the project, ensure this relative path remains valid or update configurations.
