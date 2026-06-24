from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default="E-Commerce Dynamic Price Optimizer & Churn Shield")
    API_V1_STR: str = Field(default="/api/v1")
    PRICING_MODEL_PATH: str = Field(default="app/ml_artifacts/pricer_v1.joblib")
    CHURN_MODEL_PATH: str = Field(default="app/ml_artifacts/churn_v1.joblib")
    ALLOWED_ORIGINS: list[str] = Field(default=["http://localhost:5173", "http://localhost:3000"])

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()