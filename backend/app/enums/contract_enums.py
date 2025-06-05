"""
Contract-related enums only.
Single Responsibility: Contract domain constants.
"""

from enum import Enum


class ContractStatus(str, Enum):
    """Contract lifecycle status"""
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    TERMINATED = "terminated"
    RENEWED = "renewed"


class ServiceType(str, Enum):
    """Waste collection service types"""
    WASTE = "waste"
    RECYCLING = "recycling"
    COMPOST = "compost"
    MIXED_WASTE = "mixed_waste"
    LARGE_ITEM = "large_item"
    YARD_WASTE = "yard_waste"
    HAZARDOUS_WASTE = "hazardous_waste"
    CONSTRUCTION_DEBRIS = "construction_debris"
    MEDICAL_WASTE = "medical_waste"


class BillingFrequency(str, Enum):
    """Contract billing frequencies"""
    WEEKLY = "weekly"
    BI_WEEKLY = "bi_weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUALLY = "semi_annually"
    ANNUALLY = "annually"
    ON_DEMAND = "on_demand"


class ContractType(str, Enum):
    """Contract agreement types"""
    FIXED_PRICE = "fixed_price"
    UNIT_PRICE = "unit_price"
    COST_PLUS = "cost_plus"
    PERFORMANCE_BASED = "performance_based"
    HYBRID = "hybrid"


class PaymentTerms(str, Enum):
    """Payment terms"""
    NET_15 = "net_15"
    NET_30 = "net_30"
    NET_45 = "net_45"
    NET_60 = "net_60"
    CASH_ON_DELIVERY = "cash_on_delivery"
    PREPAID = "prepaid"