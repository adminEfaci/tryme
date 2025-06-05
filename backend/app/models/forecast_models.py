"""
Forecast-related models only.
Single Responsibility: Forecast domain data models.
"""

import uuid
from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field

from .base import BaseModel
from ..enums.forecast_enums import ForecastType


class ForecastBase(SQLModel):
    """Base forecast model"""
    name: str = Field(max_length=255)
    forecast_type: ForecastType
    
    # Time Range
    forecast_start_date: date
    forecast_end_date: date
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Scope
    organization_id: Optional[uuid.UUID] = Field(default=None, foreign_key="organizations.id")
    
    # Forecast Data (JSON fields for flexibility)
    demand_forecast: Optional[str] = Field(default=None)  # JSON with daily/weekly predictions
    capacity_forecast: Optional[str] = Field(default=None)  # JSON with resource availability
    cost_forecast: Optional[str] = Field(default=None)  # JSON with financial projections
    risk_factors: Optional[str] = Field(default=None)  # JSON with identified risks
    
    # Metrics
    confidence_level: float = Field(default=80.0, ge=0, le=100)
    accuracy_score: Optional[float] = Field(default=None, ge=0, le=100)
    
    # AI/ML Model Info
    model_version: Optional[str] = Field(default=None, max_length=50)
    training_data_period: Optional[str] = Field(default=None, max_length=100)
    
    notes: Optional[str] = Field(default=None, max_length=1000)


class Forecast(ForecastBase, BaseModel, table=True):
    """
    Forecast model.
    Single Responsibility: Forecast data management.
    """
    __tablename__ = "forecasts"
    
    # Relationships will be defined after all models are created


class ForecastItemBase(SQLModel):
    """Base forecast item model"""
    forecast_id: uuid.UUID = Field(foreign_key="forecasts.id")
    
    # Date & Granularity
    forecast_date: date
    granularity: str = Field(max_length=20)  # "daily", "weekly", "monthly"
    
    # Resource Predictions
    predicted_routes: Optional[int] = Field(default=None, ge=0)
    predicted_crew_hours: Optional[float] = Field(default=None, ge=0)
    predicted_vehicles_needed: Optional[int] = Field(default=None, ge=0)
    predicted_volume_cubic_yards: Optional[float] = Field(default=None, ge=0)
    
    # Cost Predictions
    predicted_labor_cost: Optional[float] = Field(default=None, ge=0)
    predicted_fuel_cost: Optional[float] = Field(default=None, ge=0)
    predicted_maintenance_cost: Optional[float] = Field(default=None, ge=0)
    predicted_total_cost: Optional[float] = Field(default=None, ge=0)
    
    # Risk Factors
    weather_risk_factor: Optional[float] = Field(default=1.0, ge=0.1, le=5.0)
    equipment_risk_factor: Optional[float] = Field(default=1.0, ge=0.1, le=5.0)
    staffing_risk_factor: Optional[float] = Field(default=1.0, ge=0.1, le=5.0)
    
    # Confidence
    confidence_score: float = Field(default=80.0, ge=0, le=100)


class ForecastItem(ForecastItemBase, BaseModel, table=True):
    """
    Forecast item model.
    Single Responsibility: Forecast item data management.
    """
    __tablename__ = "forecast_items"
    
    # Relationships will be defined after all models are created