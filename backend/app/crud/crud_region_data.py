from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
from datetime import date
from typing import List, Optional

from app.models.region_data import RegionalCovidData
from app.schemas.region_data_schema import RegionalDataCreate

class CRUDRegionalCovidData:

    def get_latest_submission_date(self, db: Session) -> Optional[date]:
        """
        Recupera la data di sottomissione più recente presente nel database.
        """
        latest_record_tuple = db.query(RegionalCovidData.submission_date).order_by(desc(RegionalCovidData.submission_date)).first()
        return latest_record_tuple[0] if latest_record_tuple else None

    def get_by_date(
        self, 
        db: Session, 
        submission_date: date,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "desc"
    ) -> List[RegionalCovidData]:
        """
        Recupera i dati COVID regionali per una data specifica, con opzioni di ordinamento.
        """
        query = db.query(RegionalCovidData).filter(RegionalCovidData.submission_date == submission_date)

        if sort_by:
            column_to_sort = getattr(RegionalCovidData, sort_by, None)
            if column_to_sort:
                if sort_order == "asc":
                    query = query.order_by(asc(column_to_sort))
                else:
                    query = query.order_by(desc(column_to_sort))
            else:
                query = query.order_by(desc(RegionalCovidData.total_positive_cases), asc(RegionalCovidData.region_name))
        else:
            query = query.order_by(desc(RegionalCovidData.total_positive_cases), asc(RegionalCovidData.region_name))
            
        return query.all()

    def get_by_date_and_region_code(
        self, db: Session, submission_date: date, region_code: str
    ) -> Optional[RegionalCovidData]:
        """
        Recupera un singolo record di dati COVID regionali per data e codice regione.
        """
        return db.query(RegionalCovidData).filter(
            RegionalCovidData.submission_date == submission_date,
            RegionalCovidData.region_code == region_code
        ).first()

    def create_or_update_bulk(
        self, db: Session, *, data_in_list: List[RegionalDataCreate]
    ) -> List[RegionalCovidData]:
        """
        Crea nuovi record di dati COVID regionali o aggiorna quelli esistenti
        se un record per la stessa data e codice regione è già presente (UPSERT).
        Questo viene fatto per una lista di dati.
        """
        created_or_updated_records = []
        for data_in in data_in_list:
            db_obj = self.get_by_date_and_region_code(
                db, submission_date=data_in.submission_date, region_code=data_in.region_code
            )
            if db_obj:
                update_data = data_in.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(db_obj, field, value)
                db.add(db_obj)
                created_or_updated_records.append(db_obj)
            else:
                db_obj = RegionalCovidData(**data_in.model_dump())
                db.add(db_obj)
                created_or_updated_records.append(db_obj)
        
        try:
            db.commit()
            for record in created_or_updated_records:
                db.refresh(record)
        except Exception as e:
            db.rollback()
            print(f"Error during bulk create/update: {e}")
            raise
            
        return created_or_updated_records

    def create(self, db: Session, *, obj_in: RegionalDataCreate) -> RegionalCovidData:
        """
        Crea un singolo nuovo record (non usato direttamente se usiamo create_or_update_bulk).
        """
        db_obj = RegionalCovidData(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def data_exists_for_date(self, db: Session, submission_date: date) -> bool:
        """
        Controlla se esistono dati per una specifica data nel database.
        """
        return db.query(RegionalCovidData.id).filter(RegionalCovidData.submission_date == submission_date).first() is not None

regional_data = CRUDRegionalCovidData()