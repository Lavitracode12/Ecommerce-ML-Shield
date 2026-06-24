from pydantic import BaseModel, Field

class PricingOptimizationRequest(BaseModel):
    base_price: float = Field(..., gt=0.0, description="The structural base price of the item.", examples=[49.99])
    competitor_price: float = Field(..., gt=0.0, description="Current match pricing scrape from competitors.", examples=[52.50])
    stock_level: int = Field(..., ge=0, description="Available operational warehouse inventory units.", examples=[45])
    days_to_restock: int = Field(..., ge=0, description="Lead timeline days until inventory replacement.", examples=[7])
    search_velocity_multiplier: float = Field(..., ge=0.1, le=5.0, description="Normalized scalar tracking catalog impressions growth scaling.", examples=[1.4])

class PricingOptimizationResponse(BaseModel):
    recommended_price: float = Field(..., description="The dynamic algorithmic equilibrium price.")
    margin_delta: float = Field(..., description="Variance between suggested execution tier and original index configuration base.")
    confidence_score: float = Field(default=0.95, description="Statistical variance coverage probability bound.")

class ChurnAssessmentRow(BaseModel):
    customer_id: str = Field(..., description="Unique deterministic tracking hash string.")
    login_frequency: int = Field(..., ge=0, description="Monthly application portal sessions logged.")
    days_since_last_purchase: int = Field(..., ge=0, description="Stagnancy index threshold counting operational calendar intervals.")
    cart_abandonment_rate: float = Field(..., ge=0.0, le=1.0, description="Ratio boundary constraints for items abandoned inside checking vectors.")

class BatchChurnResponse(BaseModel):
    status: str = Field(..., description="Asynchronous process execution ticket notification message.")
    processed_count: int = Field(..., description="Total element records parsed out from target matrix frame.")