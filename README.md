# COVID-19 Italy Data Dashboard

This project is a web application designed to fetch, process, store, and display epidemiological data concerning the SARS-CoV-2 pandemic in Italy, as released by the Italian Civil Protection Department. This was developed as a technical homework assignment.

## Current Status & Features

**Backend (API):**

* [X] **Latest Regional Data:** Serves aggregated COVID-19 case data by Italian region for the most recent day available from the source.
* [X] **Historical Regional Data:** Allows querying for aggregated regional data for any specific date starting from February 24th, 2020.
* [X] **Data Persistence:** Fetched and processed data is stored in an SQLite database to optimize subsequent requests.
* [X] **Dynamic Sorting:** API responses can be sorted by `total_positive_cases` or `region_name` in ascending or descending order.
* [ ] **XLSX Export:** (Task #3 - To be implemented) Endpoint to export data in XLSX format.

**Frontend (User Interface):**

* [X] **Data Visualization:** Displays regional COVID-19 data in a clear, tabular format.
* [X] **Date Selection:** Users can select a specific date to view historical data, defaulting to the latest available data on initial load.
* [X] **Loading & Error States:** Provides user feedback during data fetching operations and in case of API errors.
* [ ] **Dynamic Sorting Controls:** (Task #4 - To be implemented) UI elements to allow users to change data sorting.
* [ ] **XLSX Export Trigger:** (Task #3 - To be implemented) UI button to trigger data export.

## Tech Stack

* **Backend:**
  * **Language/Framework:** Python 3.10+ with FastAPI
  * **Async Server:** Uvicorn
  * **Database:** SQLite
  * **ORM & Migrations:** SQLAlchemy & Alembic
  * **HTTP Client:** `httpx` (for asynchronous requests)
  * **Excel Export (Planned):** `openpyxl`
  * **Dependency Management:** `pip` and `requirements.txt`
* **Frontend:**
  * **Framework/Library:** React (with TypeScript)
  * **Build Tool:** Vite
  * **HTTP Client:** `axios`
  * **Package Manager:** `npm` (or `yarn`)
* **Development:**
  * **Version Control:** Git & GitHub
  * **Virtual Environments (Python):** `venv`

## Project Structure

```
COVID-DASHBOARD/
├── backend/                # FastAPI application (Python)
│   ├── alembic/            # Alembic migration scripts
│   ├── alembic.ini         # Alembic configuration
│   ├── app/                # Main application code
│   │   ├── core/           # Configuration, settings
│   │   ├── data/           # SQLite database file (auto-created)
│   │   ├── db/             # Database session, base SQLAlchemy model
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic schemas for API validation/serialization
│   │   ├── services/       # Business logic (data fetching, processing)
│   │   ├── crud/           # Data Access Layer (Create, Read, Update, Delete operations)
│   │   ├── api/            # API routers and endpoint definitions
│   │   ├── __init__.py
│   │   └── main.py         # FastAPI app instance, global middleware, startup
│   ├── tests/              # (Placeholder) Pytest unit/integration tests
│   ├── venv/               # Python virtual environment (git ignored)
│   ├── .env.example        # Example environment variables
│   ├── .env                # Local environment variables (git ignored)
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Backend specific instructions
├── frontend/
│   └── covid-dashboard/    # React application (TypeScript)
│       ├── public/         # Static assets (e.g., favicon)
│       ├── src/            # React components, services, types, styles
│       ├── .env.example    # Example environment variables for frontend
│       ├── .env            # Local frontend environment variables (git ignored)
│       ├── index.html      # Main HTML page for Vite
│       ├── package.json    # Frontend dependencies and npm scripts
│       ├── tsconfig.json   # TypeScript configuration
│       ├── vite.config.ts  # Vite configuration
│       └── README.md       # Frontend specific instructions
├── .gitignore              # Specifies intentionally untracked files
└── README.md               # This file: main project overview
```

## Prerequisites

* Python 3.10 or higher (ensure `python` and `pip` are in your PATH)
* Node.js LTS version (e.g., v18.x, v20.x) (ensure `node` and `npm` or `yarn` are in your PATH)
* Git

## Setup and Running the Application

Detailed instructions for setting up and running the backend and frontend can be found in their respective README files:

* **[Backend Setup &amp; Operations](./backend/README.md)**
* **[Frontend Setup &amp; Operations](./frontend/covid-dashboard/README.md)**

**Quick Start (summary after individual setups):**

1. **Start the Backend Server:**

   * Navigate to the `backend` directory.
   * Ensure your Python virtual environment is activated.
   * Run: `uvicorn app.main:app --reload`
   * The backend API will typically be available at `http://127.0.0.1:8000`.
   * API documentation (Swagger UI) will be at `http://127.0.0.1:8000/docs`.
2. **Start the Frontend Development Server:**

   * Navigate to the `frontend/covid-dashboard` directory.
   * Run: `npm run dev` (or `yarn dev`)
   * The frontend application will typically be available at `http://localhost:5173` (Vite's default) or another port indicated in the terminal. Open this URL in your web browser.

## Data Source

The epidemiological data is sourced from the official GitHub repository of the Italian Civil Protection Department:
[pcm-dpc/COVID-19](https://github.com/pcm-dpc/COVID-19)

Specifically, this application uses:

* The per-province JSON file for the latest data: `dati-json/dpc-covid19-ita-province-latest.json`
* The historical per-province CSV files: `dati-province/dpc-covid19-ita-province-YYYYMMDD.csv`

## Troubleshooting / Maintenance Notes

* **Backend - Data Not Updating for "Today":** If the "latest" data shown seems old, it might be because the Civil Protection Department hasn't updated their `latest.json` file yet for the current day. The application fetches what is available. The backend logs will indicate the actual date of the "latest" data fetched.
* **Backend - Database Migrations:** If you modify SQLAlchemy models (`backend/app/models/`), remember to generate and apply new Alembic migrations. See `backend/README.md` for commands.
* **Frontend - Connection to Backend:** Ensure the `VITE_API_BACKEND_URL` in `frontend/covid-dashboard/.env` correctly points to your running backend API.
* **Frontend - Cached Data/Behavior:** If the frontend behaves unexpectedly after code changes, try an "hard refresh" (Ctrl+Shift+R or Cmd+Shift+R) in your browser or clear the browser cache for the site.
* **General - Check Logs:** Both backend (terminal where Uvicorn runs) and frontend (browser's developer console) logs are invaluable for diagnosing issues.
