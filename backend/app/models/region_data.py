# backend/app/models/region_data.py
from sqlalchemy import Column, Integer, String, Date, UniqueConstraint
# from sqlalchemy.orm import relationship # Uncomment if relationships are needed

from app.db.session import Base

class RegionalCovidData(Base):
    __tablename__ = "regional_covid_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    submission_date = Column(Date, nullable=False, index=True) # Data del report
    # Consider using 'codice_regione' from JSON directly, it's numeric.
    # Using String for flexibility if codes can have non-numeric chars or leading zeros.
    region_code = Column(String, nullable=False, index=True)
    region_name = Column(String, nullable=False, index=True)
    total_positive_cases = Column(Integer, nullable=False, default=0)

    # Ensures that for a given date, each region appears only once.
    __table_args__ = (UniqueConstraint('submission_date', 'region_name', name='_submission_date_region_name_uc'),)

    def __repr__(self):
        return f"<RegionalCovidData(date='{self.submission_date}', region='{self.region_name}', cases='{self.total_positive_cases}')>"