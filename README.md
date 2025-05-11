# COVID-19 Italy Data Dashboard

This project is a full-stack web application developed to demonstrate proficiency in fetching, processing, storing, and visualizing epidemiological data concerning the SARS-CoV-2 pandemic in Italy. The data is sourced from the official repository of the Italian Civil Protection Department. This application serves as a technical homework assignment, showcasing design choices, backend and frontend development skills.

## Project Philosophy & Design Rationale

The core philosophy behind this project was to build a robust, maintainable, and reasonably efficient application adhering to modern development practices. Key considerations included:

* **Separation of Concerns:** A clear distinction between the backend (data logic, API) and the frontend (presentation, user interaction) to promote modularity and independent development.
* **Efficient Data Handling:** Implementing a local data cache (SQLite database) to minimize redundant calls to the external data source, ensuring faster response times for users and respectful usage of the public API.
* **Asynchronous Operations:** Leveraging asynchronous programming in the backend (`FastAPI`, `httpx`) to handle I/O-bound tasks like external API calls efficiently, preventing blocking and improving throughput.
* **Modern Stack:** Utilizing a contemporary and widely adopted technology stack (Python/FastAPI for backend, React/TypeScript for frontend) relevant to current industry standards.
* **Developer Experience:** Employing tools like Alembic for database migrations, Pydantic for data validation, and Vite for a fast frontend development cycle.

## Current Status & Features

**Backend (API):**

* [X] **Latest Regional Data:** Serves aggregated COVID-19 case data by Italian region for the most recent day available.
* [X] **Historical Regional Data:** Allows querying for aggregated regional data for any specific date from February 24th, 2020.
* [X] **Data Persistence & Caching:** Fetched and processed data is stored in an SQLite database.
* [X] **Dynamic Sorting:** API responses are sortable by key data fields.
* [X] **XLSX Export:** Endpoint to export currently queried/displayed data in XLSX format.

**Frontend (User Interface):**

* [X] **Data Visualization:** Displays regional data in a sortable, interactive table.
* [X] **Date Selection:** Enables users to select specific dates for historical data views.
* [X] **Dynamic Sorting Controls:** UI for users to control data sorting in the table.
* [X] **XLSX Export Trigger:** UI button to initiate data export.
* [X] **Loading & Error States:** Provides clear user feedback during operations.

## Technology Stack & Justification

The selection of technologies was driven by a balance of performance, developer productivity, ecosystem maturity, and relevance to modern web development, moreover than my personal acknowledge.

* **Backend:**

  * **Python 3.10+ & FastAPI:**
    * *Why Python?* Its extensive data science ecosystem, readability, and large community make it a strong choice for data-centric applications.
    * *Why FastAPI?* A modern, high-performance web framework built on Starlette and Pydantic. It offers asynchronous request handling out-of-the-box (crucial for I/O-bound tasks like fetching external data), automatic data validation and serialization via Pydantic, and auto-generated interactive API documentation (Swagger UI/ReDoc), significantly boosting development speed and API quality.
  * **Uvicorn:** The recommended ASGI server for FastAPI, known for its speed.
  * **SQLAlchemy & Alembic:**
    * *Why SQLAlchemy?* A powerful and flexible ORM, abstracting database interactions and allowing for database-agnostic model definitions (though SQLite is used here). Its robustness handles complex queries and relationships well.
    * *Why Alembic?* The de-facto database migration tool for SQLAlchemy, providing a controlled, versioned approach to schema evolution, essential for any production-grade application.
  * **SQLite:**
    * *Why SQLite?* Chosen for its simplicity, serverless nature, and ease of setup for this project's scope. It's file-based, requiring no separate server process, making the application highly portable and easy for an evaluator to run. For larger-scale production, transitioning to PostgreSQL or MySQL would be a natural next step, facilitated by SQLAlchemy's abstraction.
  * **`httpx`:** A modern, fully featured asynchronous HTTP client for Python, aligning perfectly with FastAPI's async nature for non-blocking external API calls. This is a better solution rather than `requests`.
  * **`openpyxl`:** The standard Python library for reading/writing Excel 2010 xlsx/xlsm/xltx/xltm files, chosen for its comprehensive feature set for the XLSX export requirement.
  * **Pydantic:** Used by FastAPI for data validation, serialization, and settings management. It ensures data integrity at the API boundary and provides clear error messages.
* **Frontend:**

  * **React (with TypeScript):**
    * *Why React?* A leading JavaScript library for building user interfaces, known for its component-based architecture, declarative programming model, and vast ecosystem.
    * *Why TypeScript?* Adds static typing to JavaScript, significantly improving code quality, maintainability, and developer experience by catching errors early and enhancing code autocompletion and refactoring.
  * **Vite:** A next-generation frontend tooling solution providing an extremely fast development server (leveraging native ES modules) and optimized builds. Chosen over Create React App for its superior speed and modern DX.
  * **`axios`:** A popular, promise-based HTTP client for the browser and Node.js, making API communication padrões and straightforward.
  * **Font Awesome (`@fortawesome/react-fontawesome`):** Integrated for a richer UI with scalable vector icons, using the React component library for optimal integration and tree-shaking.
* **Development & Tooling:**

  * **Git & GitHub:** Standard for version control and collaboration/submission.
  * **Python `venv`:** For isolated Python environments, ensuring dependency consistency.
  * **ESLint/Prettier (Assumed for Frontend):** Standard linting and code formatting tools to maintain code quality and consistency. (Mention if you actively used them).
  * **Black/Flake8 (Assumed for Backend):** Similar tools for Python. (Mention if you actively used them).
* **Development & Tooling:**

  * **Git & GitHub:** Standard for version control and collaboration/submission.
  * **Python `venv`:** For isolated Python environments, ensuring dependency consistency.
  * **Code Formatting & Linting (Recommended):**
    * *(These tools were not completely run during this exercise but I would use them for larger projects.)*
    * **Frontend (React/TypeScript):** **ESLint** (often pre-configured by Vite/CRA) for linting and **Prettier** for code formatting.
    * **Backend (Python):** **Black** for code formatting and **Flake8** (or **Ruff**) for linting.

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

## Key Design Decisions & Technical Highlights

* **API-First Approach:** The backend API was designed as a standalone service, allowing for flexible client consumption (not just the provided React frontend).
* **Asynchronous Backend:** All I/O operations in the backend (database access, external HTTP calls) are asynchronous, maximizing the application's ability to handle concurrent requests.
* **Robust Data Ingestion:** The `data_fetcher` service is designed to handle different data formats (JSON for latest, CSV for historical) and gracefully manage potential network errors or "file not found" scenarios from the source.
* **Idempotent Data Storage:** The `data_processor` and `crud` services implement an "upsert" logic, ensuring that reprocessing the same data does not lead to duplicates, and existing records are updated if necessary.
* **Clear Separation of Logic:** Services (`data_fetcher`, `data_processor`), data access (`crud`), API definitions (`api/endpoints`), and models/schemas are distinctly separated in the backend, following common design patterns for maintainability.
* **Type Safety:** TypeScript in the frontend and Pydantic type hints in the backend contribute to a more robust and less error-prone codebase.

## Troubleshooting / Maintenance Notes

* **Backend - Data Not Updating for "Today":** If the "latest" data shown seems old, it might be because the Civil Protection Department hasn't updated their `latest.json` file yet for the current day. The application fetches what is available. The backend logs will indicate the actual date of the "latest" data fetched.
* **Backend - Database Migrations:** If you modify SQLAlchemy models (`backend/app/models/`), remember to generate and apply new Alembic migrations. See `backend/README.md` for commands.
* **Frontend - Connection to Backend:** Ensure the `VITE_API_BACKEND_URL` in `frontend/covid-dashboard/.env` correctly points to your running backend API.
* **Frontend - Cached Data/Behavior:** If the frontend behaves unexpectedly after code changes, try an "hard refresh" (Ctrl+Shift+R or Cmd+Shift+R) in your browser or clear the browser cache for the site.
* **General - Check Logs:** Both backend (terminal where Uvicorn runs) and frontend (browser's developer console) logs are invaluable for diagnosing issues.
