# COVID-19 Italy Data Dashboard

This project is a web application designed to fetch, process, store, and display epidemiological data concerning the SARS-CoV-2 pandemic in Italy, as released by the Italian Civil Protection Department. This was developed as a technical homework assignment.

## Features

*   Displays the grand total of COVID-19 cases aggregated by Italian region for the current day.
*   Allows users to search for and display regional data for any specific date from February 24th, 2020, onwards.
*   Provides an option to export the displayed regional data (current day or selected date) into an `.xlsx` file.
*   Allows users to change sorting options for the displayed data directly from the web browser.

## Tech Stack

*   **Backend:**
    *   **Language/Framework:** Python 3.10+ with FastAPI
    *   **Async Server:** Uvicorn
    *   **Database:** SQLite
    *   **ORM & Migrations:** SQLAlchemy & Alembic
    *   **HTTP Client:** `httpx` (for asynchronous requests)
    *   **Excel Export:** `openpyxl`
    *   **Dependency Management:** `pip` and `requirements.txt`
*   **Frontend:**
    *   **Framework/Library:** React (with TypeScript)
    *   **Build Tool:** Vite
    *   **HTTP Client:** `axios`
    *   **Package Manager:** `npm` (or `yarn`)
*   **Development:**
    *   **Version Control:** Git & GitHub
    *   **Virtual Environments (Python):** `venv`

## Project Structure

```
COVID-DASHBOARD/
├── backend/                # FastAPI application (Python)
│   ├── alembic/            # Alembic migration scripts
│   ├── alembic.ini         # Alembic configuration
│   ├── app/                # Main application code
│   │   ├── core/           # Configuration, settings
│   │   ├── data/           # SQLite database file (created automatically)
│   │   ├── db/             # Database session, base model
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas (for API validation/serialization)
│   │   ├── services/       # Business logic (data fetching, processing)
│   │   ├── api/            # API routers/endpoints
│   │   ├── __init__.py
│   │   └── main.py         # FastAPI app instance and main startup
│   ├── tests/              # (Optional) Pytest unit/integration tests
│   ├── venv/               # Python virtual environment (ignored by git)
│   ├── .env.example        # Example environment variables
│   ├── .env                # Local environment variables (ignored by git)
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Backend specific instructions
├── frontend/
│   └── covid-dashboard/    # React application (TypeScript)
│       ├── public/         # Static assets
│       ├── src/            # React components, services, styles
│       ├── .env.example    # Example environment variables for frontend
│       ├── .env            # Local frontend environment variables (ignored by git)
│       ├── index.html      # Main HTML page for Vite
│       ├── package.json    # Frontend dependencies and scripts
│       ├── tsconfig.json   # TypeScript configuration
│       ├── vite.config.ts  # Vite configuration
│       └── README.md       # Frontend specific instructions
├── .gitignore              # Specifies intentionally untracked files
└── README.md               # This file: main project overview
```

## Prerequisites

*   Python 3.10 or higher
*   Node.js (which includes npm) LTS version (e.g., v18.x, v20.x) or Yarn
*   Git

## Setup and Running the Application

Detailed instructions for setting up and running the backend and frontend can be found in their respective README files:

*   **[Backend Setup](./backend/README.md)**
*   **[Frontend Setup](./frontend/covid-dashboard/README.md)**

**Quick Start (summary after individual setups):**

1.  **Start the Backend Server:**
    *   Navigate to the `backend` directory.
    *   Ensure your Python virtual environment is activated.
    *   Run: `uvicorn app.main:app --reload`
    *   The backend API will typically be available at `http://127.0.0.1:8000`.
    *   API documentation (Swagger UI) will be at `http://127.0.0.1:8000/docs`.

2.  **Start the Frontend Development Server:**
    *   Navigate to the `frontend/covid-dashboard` directory.
    *   Run: `npm run dev` (or `yarn dev`)
    *   The frontend application will typically be available at `http://localhost:5173` (Vite's default) or another port indicated in the terminal.

## Data Source

The epidemiological data is sourced from the official GitHub repository of the Italian Civil Protection Department:
[pcm-dpc/COVID-19](https://github.com/pcm-dpc/COVID-19)

Specifically, this application uses:
*   The per-province JSON file for the latest data: `dati-json/dpc-covid19-ita-province-latest.json`
*   The historical per-province CSV files: `dati-province/dpc-covid19-ita-province-YYYYMMDD.csv`

*(More sections like 'API Endpoints Overview', 'Contributing', 'License' could be added if this were a larger, collaborative project)*