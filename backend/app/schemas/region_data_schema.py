from pydantic import BaseModel, field_validator, Field
from datetime import date
from typing import Optional

# --- BASE MAPPING ---
class RegionalDataInDBBase(BaseModel):
    id: Optional[int] = None
    submission_date: date
    region_code: str = Field(..., min_length=1, max_length=3)
    region_name: str = Field(..., min_length=1)
    total_positive_cases: int = Field(..., ge=0) # greater than or equal to 0

    class Config:
        from_attributes = True

# --- DATA CREATION MAPPING ---
class RegionalDataCreate(RegionalDataInDBBase):
    pass

# --- API READ/RESPONSE MAPPING ---
class RegionalData(RegionalDataInDBBase):
    pass