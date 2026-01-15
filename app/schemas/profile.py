from pydantic import BaseModel, Field
from typing import Optional


class UserProfile(BaseModel):
    age: int = Field(..., ge=18, le=100)
    monthly_income: float = Field(..., gt=0)
    dependants: int = Field(..., ge=0)
    employment_type: str  # employed | self-employed | unemployed
    owns_car: bool
    owns_home: bool
