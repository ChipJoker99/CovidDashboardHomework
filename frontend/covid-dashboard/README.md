# COVID-19 Data Dashboard – Frontend

This repository contains the React frontend (using TypeScript and Vite) for the COVID-19 Data Dashboard for Italy. It provides a clean user interface for exploring regional COVID-19 statistics served by a backend API.

## Features

- **Regional Data Table**
  Displays a sortable table showing region names, total positive cases, and the date of data submission.

- **Date Picker**
  Allows users to select a historical date (from February 24th, 2020, onward) to view data for that day. Includes a "Show Latest Data" button to reset the view to the most recent records.

- **Loading States**
  Displays a loading message while fetching data from the API.

- **Error Handling**
  Shows user-friendly messages when API calls fail or data is unavailable for the selected date.

- **Dynamic Sorting**
  Column headers are clickable to sort data ascending/descending by region name and total positive cases.

- **XLSX Export**
  Allows users to export the currently displayed data (including date filters) into a `.xlsx` spreadsheet with a single click.

## Tech Stack

- React 18+
- TypeScript
- Vite (development server and build tool)
- Axios (for HTTP requests)
- `npm` for package management
- CSS (with potential use of modules or utility frameworks in larger projects)
- FontAwesome (for UI icons)

## Project Structure (within `frontend/covid-dashboard/src/`)

- `main.tsx`: The main entry point of the React application, renders the `App` component.
- `App.tsx`: The root component of the application. It manages the main state, including the selected date, fetched regional data, loading status, and error messages. It orchestrates data fetching and renders the `DateSelector` and `RegionTable` components.
- `components/`: Contains reusable UI components:
  - `RegionTable.tsx`: A functional component responsible for rendering the table of regional COVID-19 data. It receives data, loading state, and error state as props.
  - `DateSelector.tsx`: A component providing a date input field and a button to reset to the latest data. It calls back to `App.tsx` when the date changes.
  - Component-specific CSS files (e.g., `RegionTable.css`, `DateSelector.css`).
- `services/`: Modules for abstracting external interactions:
  - `apiService.ts`: Contains the `getRegionalData` function, which uses `axios` to make GET requests to the backend API's `/regions/` endpoint, handling query parameters for date and sorting.
- `types/`: TypeScript type definitions and interfaces:
  - `regionalData.ts`: Defines the `RegionalData` interface, matching the structure of data objects returned by the backend API.
- `assets/`: (If applicable) Static assets like images or fonts.
- `App.css`, `index.css`: Global and root-level styles.
- `vite-env.d.ts`: Vite-specific TypeScript definitions (e.g., `import.meta.env`).

## Setup

1.  **Navigate to the frontend project directory:**

   ```bash
   cd /frontend/covid-dashboard
   ```

2.  **Install dependencies:**

   ```bash
   npm install
   ```

3.  **Install required additional dependencies:**

If you see errors like the following:

```bash
Error: The following dependencies are imported but could not be resolved:
@fortawesome/react-fontawesome
@fortawesome/free-solid-svg-icons
```

then install them manually:

```bash
npm install @fortawesome/react-fontawesome @fortawesome/free-solid-svg-icons
```

4. **Set up environment variables:**

   - Copy the example environment file:

     ```bash
     cp .env.example .env
     ```

   - Edit `.env` and set the backend API URL:

     ```env
     VITE_API_BACKEND_URL=http://127.0.0.1:8000/api/v1
     ```

   -  The `apiService.ts` will use this variable, falling back to a default if not set.

## Available Scripts

From the `frontend/covid-dashboard` directory, you can run:

### `npm run dev`

Starts the development server with hot module replacement.
Visit [http://localhost:5173](http://localhost:5173) in your browser.

### `npm run build`

Creates an optimized production build in the dist/ folder.

### `npm run preview`

Runs a local server to preview the production build.

## Connecting to the Backend

For the frontend to function correctly, the backend server must be running and accessible at the URL specified by `VITE_API_BACKEND_URL`. If the backend is not running or is inaccessible, the frontend will display an error message when attempting to fetch data.

## Troubleshooting / Maintenance

- **"Failed to fetch" / Network Errors:**
  - Ensure the backend server is running.
  - Verify that `VITE_API_BACKEND_URL` in `.env` is correct and matches where the backend is being served.
  - Check for CORS errors in the browser's developer console. If present, the backend's CORS middleware in `app.main.py` might need adjustment for your frontend's origin.
- **Data Not Displaying / Incorrect Data:**
  - Check the browser's developer console for JavaScript errors or network request failures.
  - Inspect the "Network" tab in developer tools to see the actual API request and response. Verify the backend is returning the expected data and status code.
- **Type Errors (TypeScript):**  Ensure your type definitions in `src/types/` accurately reflect the data structure returned by the backend API. Use `import type` for type-only imports if `verbatimModuleSyntax` is enabled in `tsconfig.json`.
- **Styling Issues:**  Use browser developer tools to inspect CSS rules and troubleshoot layout problems.
- **Vite Dev Server Issues:**  If the dev server behaves erratically, try stopping it (Ctrl+C) and restarting it. Occasionally, deleting the `node_modules/.vite` cache directory and restarting can help.
