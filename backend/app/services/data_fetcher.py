import httpx
import logging
from datetime import date, datetime, timedelta
import json
import csv
import io

from app.core.config import settings

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)

JSON_BASE_URL = settings.DPC_REPO_BASE_URL
CSV_BASE_URL = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/"

LATEST_FILENAME_JSON = settings.PROVINCES_LATEST_FILENAME

DATE_FILENAME_FORMAT_CSV = "dpc-covid19-ita-province-{date_str}.csv" # date_str as YYYYMMDD

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

class DataFetchingError(Exception):
    pass

class DataNotFoundError(DataFetchingError):
    pass

async def _fetch_text_content(file_url: str, client: httpx.AsyncClient) -> str:
    """Helper per scaricare contenuto testuale e gestire errori base."""
    logger.info(f"Attempting to fetch text content from: {file_url}")
    response = await client.get(file_url)
    
    if response.status_code == 404:
        logger.warning(f"Data not found (404) at {file_url}")
        raise DataNotFoundError(f"Data not found (404) at {file_url}")
    
    response.raise_for_status()
    return response.text

async def get_latest_provincial_data() -> list[dict]:
    """
    Fetches the latest available provincial COVID-19 data (JSON format).
    """
    file_url = f"{JSON_BASE_URL}{LATEST_FILENAME_JSON}"
    logger.info(f"Attempting to fetch LATEST JSON data from: {file_url}")
    async with httpx.AsyncClient(timeout=30.0, headers=HEADERS, follow_redirects=True) as client:
        try:
            response_text = await _fetch_text_content(file_url, client)
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing LATEST JSON from {file_url}: {e}. Content: {response_text[:200]}")
            raise DataFetchingError(f"Could not parse LATEST JSON response from {file_url}") from e
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.error(f"HTTP/Request error fetching LATEST data from {file_url}: {e}")
            if isinstance(e, DataNotFoundError):
                raise
            raise DataFetchingError(f"Error fetching LATEST data from {file_url}: {str(e)}") from e


async def get_provincial_data_by_date(target_date: date) -> list[dict]:
    """
    Fetches provincial COVID-19 data for a specific date (CSV format).
    """
    if not isinstance(target_date, date):
        raise ValueError("target_date must be a datetime.date object")

    date_str = target_date.strftime("%Y%m%d")
    filename = DATE_FILENAME_FORMAT_CSV.format(date_str=date_str)
    file_url = f"{CSV_BASE_URL}{filename}"

    logger.info(f"Attempting to fetch HISTORICAL CSV data from: {file_url}")
    async with httpx.AsyncClient(timeout=30.0, headers=HEADERS, follow_redirects=True) as client:
        try:
            csv_text_content = await _fetch_text_content(file_url, client)
            
            csvfile = io.StringIO(csv_text_content)
            reader = csv.DictReader(csvfile)
            data_list = [row for row in reader]
            
            return data_list

        except DataNotFoundError:
            raise
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.error(f"HTTP/Request error fetching HISTORICAL CSV data from {file_url}: {e}")
            raise DataFetchingError(f"Error fetching HISTORICAL CSV data from {file_url}: {str(e)}") from e
        except csv.Error as e:
            logger.error(f"Error parsing CSV from {file_url}: {e}")
            raise DataFetchingError(f"Could not parse CSV response from {file_url}") from e
        except Exception as e: 
            logger.error(f"Unexpected error processing CSV from {file_url}: {e.__class__.__name__} {e}")
            raise DataFetchingError(f"Unexpected error processing CSV from {file_url}: {str(e)}") from e


# --- TEST BLOCK ---
if __name__ == "__main__":
    import asyncio

    async def main_test():
        print("--- Testing get_latest_provincial_data (JSON) ---")
        try:
            latest_data = await get_latest_provincial_data()
            print(f"Successfully fetched latest JSON data. Number of records: {len(latest_data)}")
            if latest_data:
                 print(f"First record (JSON) from latest_data: {latest_data[0]}")
        except DataFetchingError as e:
            print(f"Error fetching latest JSON data: {e}")

        print("\n--- Testing get_provincial_data_by_date (CSV - valid date: 2020-03-15) ---")
        valid_test_date_csv = date(2020, 3, 15)
        try:
            csv_data = await get_provincial_data_by_date(valid_test_date_csv)
            print(f"Successfully fetched CSV data for {valid_test_date_csv}. Number of records: {len(csv_data)}")
            if csv_data:
                print(f"First record (CSV) for {valid_test_date_csv}: {csv_data[0]}")
        except DataFetchingError as e:
            print(f"Error fetching CSV data for {valid_test_date_csv}: {e}")

        print("\n--- Testing get_provincial_data_by_date (CSV - first available date: 2020-02-24) ---")
        first_available_date_csv = date(2020, 2, 24)
        try:
            csv_data_first = await get_provincial_data_by_date(first_available_date_csv)
            print(f"Successfully fetched CSV data for {first_available_date_csv}. Number of records: {len(csv_data_first)}")
            if csv_data_first:
                 print(f"First record (CSV) for {first_available_date_csv}: {csv_data_first[0]}")
        except DataFetchingError as e:
            print(f"Error fetching CSV data for {first_available_date_csv}: {e}")

        print("\n--- Testing get_provincial_data_by_date (CSV - date likely not found: 2020-02-01) ---")
        not_found_test_date_csv = date(2020, 2, 1)
        try:
            await get_provincial_data_by_date(not_found_test_date_csv)
            print(f"Fetched CSV data for {not_found_test_date_csv}, but expected DataNotFoundError.")
        except DataNotFoundError:
            print(f"Correctly caught DataNotFoundError for {not_found_test_date_csv} (CSV - expected).")
        except DataFetchingError as e:
            print(f"Error fetching CSV data for {not_found_test_date_csv}: {e}")
        
        print("\n--- Testing get_provincial_data_by_date (CSV - future date) ---")
        future_test_date_csv = date.today() + timedelta(days=30)
        try:
            await get_provincial_data_by_date(future_test_date_csv)
            print(f"Fetched CSV data for {future_test_date_csv}, but expected DataNotFoundError.")
        except DataNotFoundError:
            print(f"Correctly caught DataNotFoundError for {future_test_date_csv} (CSV - expected).")
        except DataFetchingError as e:
            print(f"Error fetching CSV data for {future_test_date_csv}: {e}")

    asyncio.run(main_test())