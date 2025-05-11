# COVID-19 Data API - Backend

This directory contains the Python FastAPI backend for the COVID-19 Italy Data Dashboard. Its primary role is to serve processed and aggregated epidemiological data to the frontend client.

## Responsibilities

* **Data Ingestion:** Fetches raw provincial data (JSON for latest, CSV for historical) from the DPC's GitHub repository.
* **Data Processing:** Validates, cleans, and aggregates provincial case data to calculate regional totals. Converts data types as needed.
* **Data Persistence:** Stores processed regional data in a local SQLite database using SQLAlchemy ORM, with Alembic managing schema migrations. Implements an "upsert" logic to avoid data duplication for a given date and region.
* **API Exposure:** Provides RESTful API endpoints for the frontend to retrieve regional data, supporting date-specific queries and dynamic sorting.
* **Error Handling:** Implements error handling for data fetching, processing, and database operations, returning appropriate HTTP status codes.
* **(Planned) Data Export:** Will provide an endpoint to export data in `.xlsx` format.

## Tech Stack

* Python 3.10+
* FastAPI & Uvicorn (ASGI server)
* SQLAlchemy (ORM) & Alembic (Database Migrations)
* SQLite (Database)
* `httpx` (Asynchronous HTTP Client)
* `openpyxl` (For Excel generation - planned)
* Pydantic (Data validation and serialization)
* `python-dotenv` (Environment variable management)

## Project Structure (within `backend/app/`)

* `main.py`: FastAPI application entry point, global middleware (CORS, central logging configuration), and API router inclusion.
* `core/`: Application settings (`config.py` for database URLs, external source URLs, etc.).
* `db/`: Database session management (`session.py`), base SQLAlchemy model.
* `data/`: Contains the `covid_data.db` SQLite file (auto-created by Alembic or on first app run if directory doesn't exist).
* `models/`: SQLAlchemy ORM model definitions (e.g., `region_data.py` defining the `RegionalCovidData` table).
* `schemas/`: Pydantic schemas for data validation and API request/response serialization (e.g., `region_data_schema.py`).
* `services/`: Core business logic modules:
  * `data_fetcher.py`: Responsible for fetching raw data (JSON/CSV) from the DPC GitHub source. Handles network errors and source-specific data quirks.
  * `data_processor.py`: Takes raw data from the fetcher, cleans it, converts types (e.g., string dates to date objects, case numbers to integers), and aggregates provincial data into regional totals.
* `crud/`: Data Access Layer (DAL) functions.
  * `crud_region_data.py`: Contains functions for Create, Read, Update, Delete (CRUD) operations on the `RegionalCovidData` table (e.g., fetching by date, bulk create/update).
* `api/`: FastAPI router definitions.
  * `api_v1/endpoints/`: Contains modules for specific groups of endpoints.
    * `regions.py`: Defines endpoints related to regional COVID-19 data retrieval (e.g., `GET /api/v1/regions/`).
    * *(export.py: To be added for XLSX export functionality)*

## Setup

1. **Navigate to the `backend` directory:**

   ```bash
   cd path/to/your/project/COVID-DASHBOARD/backend
   ```
2. **Create and activate a Python virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
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

### Root Endpoint

* **Endpoint:** `GET /`
* **Description:** A simple root endpoint, primarily for a basic health check or welcome message.
* **Response:** A JSON object: `{"message": "Welcome to the COVID-19 Data API!"}`

## Troubleshooting / Maintenance

* **`sqlite3.OperationalError: unable to open database file` (Alembic):** Ensure the `backend/app/data/` directory exists and is writable. The `sqlalchemy.url` in `alembic.ini` should be `sqlite:///./app/data/covid_data.db` (relative to `backend/`).
* **Data Fetching Issues (404s, etc.):**
  * Verify the URLs in `app/core/config.py` (`DPC_REPO_BASE_URL`, etc.) are correct and the DPC repository structure hasn't changed.
  * Check network connectivity.
  * Examine logs from `uvicorn` for detailed error messages from `data_fetcher.py`.
* **Data Processing Issues:** Check `data_processor.py` logs for errors related to data parsing or aggregation. Ensure source data format (JSON/CSV fields) matches expectations.
* **CORS Errors from Frontend:** Ensure `app.main.py` has `CORSMiddleware` configured correctly, and the frontend's origin (e.g., `http://localhost:5173`) is in the `allow_origins` list.
