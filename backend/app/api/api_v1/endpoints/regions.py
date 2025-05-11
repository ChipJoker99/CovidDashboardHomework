from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List, Optional
import logging

from app.db.session import get_db
from app.schemas.region_data_schema import RegionalData as RegionalDataSchema
from app.crud.crud_region_data import regional_data as crud_regional_data
from app.services import data_fetcher, data_processor

router = APIRouter()
logger = logging.getLogger(__name__)

# --- HELPER FUNCTION TO PROCESS AND STORE DATA ---
async def _get_and_process_data_for_date(
    target_date: date, 
    db: Session
) -> List[RegionalDataSchema]:
    """
    INTERNAL HELPER FUNCTION TO:
    1. Check if the data exists in the database.
    2. If it doesn't, fetch it from the source, process it, and save it to the database.
    3. Retrieve the data from the database and return it.
    """

    if not crud_regional_data.data_exists_for_date(db, submission_date=target_date):
        logger.info(f"Data for {target_date} not found in DB. Fetching from source...")
        try:
            if target_date == date.today():
                raw_data = await data_fetcher.get_latest_provincial_data()
            else:
                raw_data = await data_fetcher.get_provincial_data_by_date(target_date)
            
            if not raw_data:
                logger.warning(f"No raw data fetched for {target_date}. Source might be empty or inaccessible.")
                raise HTTPException(status_code=404, detail=f"No raw data could be fetched for {target_date} from the source.")

            processed_data_list = data_processor.process_provincial_data(raw_data)

            if not processed_data_list:
                logger.warning(f"Raw data for {target_date} was fetched but processing resulted in an empty list.")
                raise HTTPException(status_code=500, detail=f"Data for {target_date} was fetched but could not be processed successfully.")

            data_to_create = []
            actual_report_date = None
            for pd in processed_data_list:
                if actual_report_date is None:
                    actual_report_date = pd.get("submission_date")
                elif actual_report_date != pd.get("submission_date"):
                    logger.error("Inconsistent submission dates found after processing. This should not happen.")
                    raise HTTPException(status_code=500, detail="Internal server error: inconsistent data processing.")
                
                pd["submission_date"] = actual_report_date
                data_to_create.append(RegionalDataSchema.model_validate(pd))

            create_schemas = [RegionalDataSchema.model_validate(item) for item in processed_data_list]

            crud_regional_data.create_or_update_bulk(db=db, data_in_list=create_schemas)
            logger.info(f"Data for {actual_report_date or target_date} fetched, processed, and saved to DB.")
            
            if actual_report_date and actual_report_date != target_date:
                logger.info(f"Original target_date was {target_date}, but actual data fetched is for {actual_report_date}.")
                db_records = crud_regional_data.get_by_date(db, submission_date=actual_report_date)
            else:
                db_records = crud_regional_data.get_by_date(db, submission_date=target_date)


        except data_fetcher.DataNotFoundError:
            logger.warning(f"Data not found at source for {target_date}.")
            raise HTTPException(status_code=404, detail=f"Data not available for date {target_date} from the source.")
        except data_fetcher.DataFetchingError as e:
            logger.error(f"Error fetching data from source for {target_date}: {e}")
            raise HTTPException(status_code=502, detail=f"Failed to fetch data from external source for {target_date}.")
        except data_processor.DataProcessingError as e:
            logger.error(f"Error processing data for {target_date}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to process data for {target_date}.")
        except Exception as e:
            logger.error(f"Unexpected error while getting or processing data for {target_date}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="An unexpected internal server error occurred.")
    else:
        logger.info(f"Data for {target_date} found in DB. Retrieving...")
        db_records = crud_regional_data.get_by_date(db, submission_date=target_date)

    if not db_records:
        logger.warning(f"No data found for {target_date} even after attempting to fetch/retrieve.")
        raise HTTPException(status_code=404, detail=f"No data available for date {target_date}.")

    return [RegionalDataSchema.model_validate(record) for record in db_records]


@router.get(
    "/", # REQUEST TO /api/v1/regions/
    response_model=List[RegionalDataSchema],
    summary="Get regional COVID-19 data",
    description="Fetches COVID-19 case data aggregated by Italian region. "
                "Data can be retrieved for a specific date or for the latest available day."
)
async def get_regional_data(
    report_date: Optional[date] = Query(None, description="Date in YYYY-MM-DD format. If not provided, defaults to today."),
    sort_by: Optional[str] = Query(None, description="Field to sort by (e.g., 'total_positive_cases', 'region_name')."),
    sort_order: Optional[str] = Query("desc", description="Sort order ('asc' or 'desc'). Default is 'desc' for cases, 'asc' for names.", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve COVID-19 data aggregated by region.
    - If `report_date` is not provided, data for the current day (or latest available) is returned.
    - If `report_date` is provided, data for that specific day is returned.
    - Data is fetched from the source if not already in the local database for the requested date.
    - Default sorting is by total cases (descending) then region name (ascending).
    """
    target_date = report_date if report_date else date.today()
    
    logger.info(f"Request received for regional data. Target date: {target_date}, Sort by: {sort_by}, Sort order: {sort_order}")

    await ensure_data_is_available(target_date, db)

    try:
        db_records = crud_regional_data.get_by_date(
            db, 
            submission_date=target_date, 
            sort_by=sort_by, 
            sort_order=sort_order.lower() if sort_order else "desc"
        )
        if not db_records:
            if target_date == date.today():
                latest_date_in_db = crud_regional_data.get_latest_submission_date(db)
                if latest_date_in_db:
                    logger.info(f"No data for today ({target_date}), attempting to retrieve for latest available date in DB: {latest_date_in_db}")
                    db_records = crud_regional_data.get_by_date(
                        db, 
                        submission_date=latest_date_in_db, 
                        sort_by=sort_by, 
                        sort_order=sort_order.lower() if sort_order else "desc"
                    )
            
            if not db_records:
                 raise HTTPException(status_code=404, detail=f"No data available for date {target_date} or latest.")

        return [RegionalDataSchema.model_validate(record) for record in db_records]
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving regional data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected internal server error occurred while retrieving data.")


async def ensure_data_is_available(target_date: date, db: Session):
    """
    Ensures that data for the target_date exists in the database.
    If not, it fetches it from the source, processes it, and saves it.
    Raises an HTTPException in case of failure.
    """
    if not crud_regional_data.data_exists_for_date(db, submission_date=target_date):
        logger.info(f"Data for {target_date} not found in DB. Fetching from source...")
        try:
            source_to_fetch = target_date
            is_today_request = (target_date == date.today())

            if is_today_request:
                raw_data = await data_fetcher.get_latest_provincial_data()
            else:
                raw_data = await data_fetcher.get_provincial_data_by_date(target_date)
            
            if not raw_data:
                raise HTTPException(status_code=404, detail=f"No raw data for {source_to_fetch} from source.")

            processed_data_list = data_processor.process_provincial_data(raw_data)
            if not processed_data_list:
                raise HTTPException(status_code=500, detail=f"Data for {source_to_fetch} fetched but could not be processed.")

            actual_report_date = processed_data_list[0].get("submission_date") if processed_data_list else None
            if not actual_report_date:
                 raise HTTPException(status_code=500, detail="Processed data is missing submission date.")
            
            if not crud_regional_data.data_exists_for_date(db, submission_date=actual_report_date):
                create_schemas = [RegionalDataSchema.model_validate(item) for item in processed_data_list]
                crud_regional_data.create_or_update_bulk(db=db, data_in_list=create_schemas)
                logger.info(f"Data for {actual_report_date} fetched, processed, and saved to DB.")
            elif is_today_request and target_date != actual_report_date:
                 logger.info(f"Data for 'today' ({target_date}) was requested. 'Latest' data is for {actual_report_date} and already exists in DB. No new save needed.")
            else:
                 logger.info(f"Data for {actual_report_date} already exists in DB or was just processed for a different target_date. No new save needed here.")


        except data_fetcher.DataNotFoundError:
            raise HTTPException(status_code=404, detail=f"Data not available for {target_date} from source.")
        except data_fetcher.DataFetchingError as e:
            raise HTTPException(status_code=502, detail=f"Failed to fetch from external source for {target_date}: {e}")
        except data_processor.DataProcessingError as e:
            raise HTTPException(status_code=500, detail=f"Failed to process data for {target_date}: {e}")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in ensure_data_is_available for {target_date}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error ensuring data availability.")