
# COVID-19 Data Dashboard - Frontend

This directory hosts the React (with TypeScript and Vite) frontend application for the COVID-19 Italy Data Dashboard. It provides a user interface to interact with and visualize the data served by the backend API.

## Current Features

* **Regional Data Display:** Fetches regional COVID-19 data from the backend and displays it in a sortable table, showing region name, total positive cases, and submission date.
* **Date Selection:** Includes a date picker allowing users to select a specific historical date (from February 24th, 2020, to the current day) to view corresponding data. A "Show Latest Data" button resets the view to the most recent data.
* **Loading Indicators:** Shows a "Loading data..." message while data is being fetched from the API.
* **Error Handling:** Displays user-friendly error messages if API calls fail or if no data is available for the selected criteria.
* **(Planned) Dynamic Sorting Controls:** UI elements to change table sorting order will be added.
* **(Planned) XLSX Export:** A button to trigger an XLSX export of the currently displayed data will be added.

## Tech Stack

* React 18+
* TypeScript
* Vite (Build tool and development server)
* `axios` (HTTP client for API communication)
* `npm` (or `yarn`) for package management
* CSS (for styling, potentially with CSS Modules or a utility-first framework in a larger project)

## Project Structure (within `frontend/covid-dashboard/src/`)

* `main.tsx`: The main entry point of the React application, renders the `App` component.
* `App.tsx`: The root component of the application. It manages the main state, including the selected date, fetched regional data, loading status, and error messages. It orchestrates data fetching and renders the `DateSelector` and `RegionTable` components.
* `components/`: Contains reusable UI components:
  * `RegionTable.tsx`: A functional component responsible for rendering the table of regional COVID-19 data. It receives data, loading state, and error state as props.
  * `DateSelector.tsx`: A component providing a date input field and a button to reset to the latest data. It calls back to `App.tsx` when the date changes.
  * Component-specific CSS files (e.g., `RegionTable.css`, `DateSelector.css`).
* `services/`: Modules for abstracting external interactions:
  * `apiService.ts`: Contains the `getRegionalData` function, which uses `axios` to make GET requests to the backend API's `/regions/` endpoint, handling query parameters for date and sorting.
* `types/`: TypeScript type definitions and interfaces:
  * `regionalData.ts`: Defines the `RegionalData` interface, matching the structure of data objects returned by the backend API.
* `assets/`: (If any) Static assets like images or custom fonts.
* `App.css`, `index.css`: Global and root-level stylesheets.
* `vite-env.d.ts`: TypeScript definitions for Vite-specific environment variables (like `import.meta.env`).

## Setup

1. **Navigate to the frontend project directory:**

   ```bash
   cd path/to/your/project/COVID-DASHBOARD/frontend/covid-dashboard
   ```
2. **Install dependencies:**
   Using npm:

   ```bash
   npm install
   ```

   Or using Yarn:

   ```bash
   yarn install
   ```
3. **Environment Variables:**

   * The frontend needs to know the base URL of the backend API.
   * If it doesn't exist, copy the example environment file:
     ```bash
     cp .env.example .env
     ```
   * Edit `frontend/covid-dashboard/.env` (this file is git ignored) and set the `VITE_API_BACKEND_URL` variable. For local development with the backend running on port 8000, this would typically be:
     ```env
     VITE_API_BACKEND_URL=http://127.0.0.1:8000/api/v1
     ```
   * The `apiService.ts` will use this variable, falling back to a default if not set.

## Available Scripts

In the `frontend/covid-dashboard` directory, you can run the following npm/yarn scripts:

### `npm run dev` or `yarn dev`

Runs the app in development mode using Vite. This enables Hot Module Replacement (HMR) for fast updates during development.
Open [http://localhost:5173](http://localhost:5173) (or the port shown in your terminal, Vite's default) to view it in your browser.
The page will automatically reload if you make edits to the code. You will also see any lint or TypeScript errors in the console.

### `npm run build` or `yarn build`

Builds the app for production to the `dist` folder.
It correctly bundles React in production mode and optimizes the build for the best performance. The build is minified, and filenames include hashes for caching.

### `npm run preview` or `yarn preview`

Serves the production build from the `dist` folder locally. This command is useful for verifying that the production build works correctly before deploying it to a hosting service.

## Connecting to the Backend

For the frontend to function correctly, the backend server must be running and accessible at the URL specified by `VITE_API_BACKEND_URL`. If the backend is not running or is inaccessible, the frontend will display an error message when attempting to fetch data.

## Troubleshooting / Maintenance

* **"Failed to fetch" / Network Errors:**
  * Ensure the backend server is running.
  * Verify that `VITE_API_BACKEND_URL` in `.env` is correct and matches where the backend is being served.
  * Check for CORS errors in the browser's developer console. If present, the backend's CORS middleware in `app.main.py` might need adjustment for your frontend's origin.
* **Data Not Displaying / Incorrect Data:**
  * Check the browser's developer console for JavaScript errors or network request failures.
  * Inspect the "Network" tab in developer tools to see the actual API request and response. Verify the backend is returning the expected data and status code.
* **Type Errors (TypeScript):** Ensure your type definitions in `src/types/` accurately reflect the data structure returned by the backend API. Use `import type` for type-only imports if `verbatimModuleSyntax` is enabled in `tsconfig.json`.
* **Styling Issues:** Use browser developer tools to inspect CSS rules and troubleshoot layout problems.
* **Vite Dev Server Issues:** If the dev server behaves erratically, try stopping it (Ctrl+C) and restarting it. Occasionally, deleting the `node_modules/.vite` cache directory and restarting can help.
