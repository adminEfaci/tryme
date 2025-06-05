"""
Forecast-related enums only.
Single Responsibility: Forecast domain constants.
"""

from enum import Enum


class ForecastType(str, Enum):
    """Forecasting model types"""
    CAPACITY_PLANNING = "capacity_planning"
    DEMAND_FORECAST = "demand_forecast"
    RESOURCE_ALLOCATION = "resource_allocation"
    COST_PROJECTION = "cost_projection"
    REVENUE_FORECAST = "revenue_forecast"
    RISK_ASSESSMENT = "risk_assessment"
    SEASONAL_ADJUSTMENT = "seasonal_adjustment"
    WEATHER_IMPACT = "weather_impact"


class ForecastStatus(str, Enum):
    """Forecast lifecycle status"""
    GENERATING = "generating"
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    OUTDATED = "outdated"


class ForecastAccuracy(str, Enum):
    """Forecast accuracy classifications"""
    EXCELLENT = "excellent"    # >95%
    GOOD = "good"             # 85-95%
    FAIR = "fair"             # 75-85%
    POOR = "poor"             # 60-75%
    UNRELIABLE = "unreliable" # <60%


class ForecastHorizon(str, Enum):
    """Forecast time horizons"""
    SHORT_TERM = "short_term"     # 1-3 months
    MEDIUM_TERM = "medium_term"   # 3-6 months
    LONG_TERM = "long_term"       # 6-12 months
    STRATEGIC = "strategic"       # 12+ months


class SeasonalPattern(str, Enum):
    """Seasonal patterns in waste collection"""
    SPRING_INCREASE = "spring_increase"
    SUMMER_PEAK = "summer_peak"
    FALL_CLEANUP = "fall_cleanup"
    WINTER_REDUCTION = "winter_reduction"
    HOLIDAY_IMPACT = "holiday_impact"
    BACK_TO_SCHOOL = "back_to_school"


class RiskFactor(str, Enum):
    """Risk factors for forecasting"""
    WEATHER = "weather"
    EQUIPMENT_FAILURE = "equipment_failure"
    STAFF_SHORTAGE = "staff_shortage"
    FUEL_PRICE = "fuel_price"
    REGULATORY_CHANGE = "regulatory_change"
    ECONOMIC_DOWNTURN = "economic_downturn"
    PANDEMIC = "pandemic"
    NATURAL_DISASTER = "natural_disaster"