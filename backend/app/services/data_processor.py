import logging
from datetime import date, datetime
from collections import defaultdict
from typing import List, Dict, Any, Union

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)

class DataProcessingError(Exception):
    """Custom exception for data processing errors."""
    pass

def _parse_date_from_string(date_str: str) -> date:
    """
    Parses a date string (YYYY-MM-DDTHH:MM:SS) into a date object.
    Returns only the date part.
    """
    try:
        return datetime.fromisoformat(date_str.split('T')[0]).date()
    except (ValueError, TypeError) as e:
        logger.error(f"Error parsing date string: '{date_str}'. Error: {e}")
        raise DataProcessingError(f"Invalid date format: '{date_str}'") from e

def _get_int_value(value: Any, field_name: str, record_identifier: str) -> int:
    """
    Safely converts a value to an integer.
    Handles empty strings or None by returning 0.
    Raises DataProcessingError for unparseable non-empty strings.
    """
    if value is None or str(value).strip() == "":
        return 0
    try:
        return int(value)
    except (ValueError, TypeError) as e:
        logger.error(f"Error converting '{field_name}' to int for record '{record_identifier}'. Value: '{value}', Type: {type(value)}. Error: {e}")
        raise DataProcessingError(f"Invalid value for '{field_name}': '{value}'. Expected an integer or empty string.") from e

def process_provincial_data(
    raw_data_list: List[Dict[str, Any]], 
    source_type: str = "json"
) -> List[Dict[str, Any]]:
    """
    Processes a list of raw provincial data (either from JSON or CSV source)
    and aggregates it by region.

    Args:
        raw_data_list: A list of dictionaries, where each dictionary
                       represents a province's data.
        source_type: Indicates if the source was 'json' or 'csv' to handle
                     potential minor differences in field names if any (though ideally they are consistent).

    Returns:
        A list of dictionaries, where each dictionary contains aggregated
        data for a region:
        {
            "submission_date": date_object,
            "region_code": str,
            "region_name": str,
            "total_positive_cases": int
        }
    
    Raises:
        DataProcessingError: If critical data is missing or unparseable.
    """
    if not raw_data_list:
        logger.warning("Received empty raw_data_list for processing.")
        return []

    aggregated_regions = defaultdict(lambda: {"total_positive_cases": 0, "submission_date": None, "region_name": None, "region_code": None})
    
    report_date: Union[date, None] = None

    for i, province_record in enumerate(raw_data_list):
        try:
            # --- NORMALIZATION & VALIDATION ---
            current_record_date_str = province_record.get("data")
            if not current_record_date_str:
                raise DataProcessingError(f"Missing 'data' field in record #{i+1}: {province_record}")
            
            current_record_date = _parse_date_from_string(current_record_date_str)

            if report_date is None:
                report_date = current_record_date
            elif report_date != current_record_date:
                logger.warning(
                    f"Inconsistent dates within the same dataset. Expected {report_date}, "
                    f"but found {current_record_date} in record #{i+1}. Using the first date found."
                )

            # --- REGION CODE ---
            region_code = province_record.get("codice_regione")
            if region_code is None:
                raise DataProcessingError(f"Missing 'codice_regione' field in record #{i+1}: {province_record}")
            region_code_str = str(region_code).strip()
            if not region_code_str:
                 raise DataProcessingError(f"Empty 'codice_regione' field in record #{i+1}: {province_record}")


            # --- REGION NAME ---
            region_name = province_record.get("denominazione_regione")
            if not region_name or not str(region_name).strip():
                raise DataProcessingError(f"Missing or empty 'denominazione_regione' field in record #{i+1}: {province_record}")
            region_name_str = str(region_name).strip()

            # --- TOTAL CASES ---
            total_cases_province_val = province_record.get("totale_casi")
            total_cases_province = _get_int_value(total_cases_province_val, "totale_casi", f"record #{i+1} (Prov: {province_record.get('denominazione_provincia')})")

            # --- AGGREGATION ---
            key = region_code_str 
            
            if aggregated_regions[key]["submission_date"] is None:
                aggregated_regions[key]["submission_date"] = report_date
                aggregated_regions[key]["region_name"] = region_name_str
                aggregated_regions[key]["region_code"] = region_code_str
            
            aggregated_regions[key]["total_positive_cases"] += total_cases_province

        except DataProcessingError as e:
            logger.error(f"Skipping record due to processing error: {e}. Record: {province_record}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error processing record #{i+1}: {province_record}. Error: {e}")
            continue

    if not aggregated_regions and raw_data_list:
        logger.error("No regions could be aggregated, but raw data was present. Check for systematic data issues.")

    return list(aggregated_regions.values())


# --- TEST MODULES ---
if __name__ == "__main__":
    # --- JSON TEST MODULE ---
    sample_json_data = [
        {'data': '2025-01-08T17:00:00', 'codice_regione': 13, 'denominazione_regione': 'Abruzzo', 'codice_provincia': 66, 'denominazione_provincia': "L'Aquila", 'totale_casi': 100},
        {'data': '2025-01-08T17:00:00', 'codice_regione': 13, 'denominazione_regione': 'Abruzzo', 'codice_provincia': 67, 'denominazione_provincia': "Pescara", 'totale_casi': 150},
        {'data': '2025-01-08T17:00:00', 'codice_regione': 12, 'denominazione_regione': 'Lazio',   'codice_provincia': 58, 'denominazione_provincia': "Roma", 'totale_casi': 1000},
        {'data': '2025-01-08T17:00:00', 'codice_regione': 12, 'denominazione_regione': 'Lazio',   'codice_provincia': 59, 'denominazione_provincia': "Latina", 'totale_casi': 200},
        {'data': '2025-01-08T17:00:00', 'codice_regione': 13, 'denominazione_regione': 'Abruzzo', 'codice_provincia': 66, 'denominazione_provincia': "L'Aquila", 'totale_casi': ''}, # Test caso vuoto
        {'data': '2025-01-08T17:00:00', 'codice_regione': 12, 'denominazione_regione': 'Lazio',   'codice_provincia': 60, 'denominazione_provincia': "Viterbo", 'totale_casi': None}, # Test None
    ]

    # --- CSV TEST MODULE ---
    sample_csv_data = [
        {'data': '2020-03-15T17:00:00', 'codice_regione': '13', 'denominazione_regione': 'Abruzzo', 'codice_provincia': '066', 'denominazione_provincia': "L'Aquila", 'totale_casi': '15'},
        {'data': '2020-03-15T17:00:00', 'codice_regione': '13', 'denominazione_regione': 'Abruzzo', 'codice_provincia': '067', 'denominazione_provincia': "Pescara", 'totale_casi': '25'},
        {'data': '2020-03-15T17:00:00', 'codice_regione': '12', 'denominazione_regione': 'Lazio',   'codice_provincia': '058', 'denominazione_provincia': "Roma", 'totale_casi': '300'},
        {'data': '2020-03-15T17:00:00', 'codice_regione': '12', 'denominazione_regione': 'Lazio',   'codice_provincia': '059', 'denominazione_provincia': "Latina", 'totale_casi': '50'},
        {'data': '2020-03-15T17:00:00', 'codice_regione': '12', 'denominazione_regione': 'Lazio',   'codice_provincia': '059', 'denominazione_provincia': "Latina", 'totale_casi': ''}, # Test stringa vuota
        # --- MISSING 'denominazione_regione'
        {'data': '2020-03-15T17:00:00', 'codice_regione': '11', 'denominazione_provincia': "Arezzo", 'totale_casi': '10'},
        # --- ERROR 'totale_casi' (STR instead of INT)
        {'data': '2020-03-15T17:00:00', 'codice_regione': '09', 'denominazione_regione': 'Toscana', 'codice_provincia': '048', 'denominazione_provincia': "Firenze", 'totale_casi': 'XYZ'},
    ]

    print("--- Processing Sample JSON Data ---")
    try:
        processed_json = process_provincial_data(sample_json_data, source_type="json")
        for region_data in processed_json:
            print(region_data)
    except DataProcessingError as e:
        print(f"Error processing JSON data: {e}")
    
    print("\n--- Processing Sample CSV Data ---")
    try:
        processed_csv = process_provincial_data(sample_csv_data, source_type="csv")
        for region_data in processed_csv:
            print(region_data)
    except DataProcessingError as e:
        print(f"Error processing CSV data: {e}")

    print("\n--- Processing Empty Data ---")
    processed_empty = process_provincial_data([])
    print(processed_empty)

    print("\n--- Processing Data with only bad records ---")
    bad_data_only = [
        {'data': '2020-03-15T17:00:00', 'codice_regione': '11', 'totale_casi': '10'},
        {'data': '2020-03-15T17:00:00', 'codice_regione': '09', 'denominazione_regione': 'Toscana', 'totale_casi': 'XYZ'}
    ]
    processed_bad = process_provincial_data(bad_data_only)
    if not processed_bad:
        print("Correctly returned empty list for data with only bad records.")
    else:
        print(f"Processed bad data: {processed_bad}")