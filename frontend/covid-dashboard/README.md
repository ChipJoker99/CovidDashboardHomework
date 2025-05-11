# COVID-19 Data Dashboard - Frontend

This directory contains the React (with TypeScript and Vite) frontend application for displaying COVID-19 data for Italy.

## Responsibilities

*   Providing a user interface to view regional COVID-19 data.
*   Allowing users to select a specific date to view historical data.
*   Enabling users to export data to an `.xlsx` file.
*   Offering options to sort the displayed data.
*   Communicating with the backend API to fetch and send data.

## Tech Stack

*   React 18+
*   TypeScript
*   Vite (build tool and development server)
*   `axios` (for HTTP requests to the backend API)
*   `npm` (or `yarn`) for package management

## Project Structure (within `frontend/covid-dashboard/src/`)

*   `main.tsx`: Entry point of the React application.
*   `App.tsx`: Main application component, routing (if any).
*   `components/`: Reusable UI components (e.g., `RegionTable.tsx`, `DatePicker.tsx`).
*   `services/`: Modules for interacting with the backend API (e.g., `apiService.ts`).
*   `hooks/`: Custom React hooks.
*   `contexts/`: React context for state management (if used).
*   `pages/`: Top-level components representing different views/pages.
*   `assets/`: Static assets like images, fonts (if not in `public/`).
*   `styles/`: Global styles, CSS modules.
*   `vite-env.d.ts`: TypeScript definitions for Vite environment variables.

## Setup

1.  **Navigate to the `frontend/covid-dashboard` directory:**
    ```bash
    cd path/to/your/project/COVID-DASHBOARD/frontend/covid-dashboard
    ```

2.  **Install dependencies:**
    Using npm:
    ```bash
    npm install
    ```
    Or using Yarn:
    ```bash
    yarn
    ```

3.  **Environment Variables:**
    *   This frontend application might need to know the base URL of the backend API.
    *   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    *   Modify `frontend/covid-dashboard/.env` to set `VITE_API_BACKEND_URL` (e.g., `VITE_API_BACKEND_URL=http://127.0.0.1:8000/api`).
        The default in the code usually points to a standard local backend URL.

## Available Scripts

In the `frontend/covid-dashboard` directory, you can run several commands:

### `npm run dev` or `yarn dev`

Runs the app in development mode with Hot Module Replacement (HMR).
Open [http://localhost:5173](http://localhost:5173) (or the port shown in your terminal) to view it in the browser.
The page will reload if you make edits. You will also see any lint errors in the console.

### `npm run build` or `yarn build`

Builds the app for production to the `dist` folder.
It correctly bundles React in production mode and optimizes the build for the best performance.
The build is minified and the filenames include hashes.

### `npm run preview` or `yarn preview`

Serves the production build from the `dist` folder locally. This is a good way to check if the production build works correctly before deploying.

## Connecting to the Backend

Ensure the backend server is running. The frontend will make API calls to the URL specified by the `VITE_API_BACKEND_URL` environment variable (or a default if not set).