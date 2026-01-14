from pydantic import BaseModel, Field
from typing import Literal, List


class RecommendationRequest(BaseModel):
    product_category: Literal[
        "life", "funeral", "health", "vehicle", "home", "travel"
    ]
    age: int = Field(..., ge=18, le=100)
    monthly_budget: float = Field(..., gt=0)
    province: str
    monthly_income: float
    risk_preference: Literal["low", "medium", "high"]


class RecommendationItem(BaseModel):
    product_id: str
    company_name: str
    product_name: str
    premium_estimate: float
    score: float
    reasons: List[str]


class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]
