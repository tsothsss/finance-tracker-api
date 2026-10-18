from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class BillingCycle(str, Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELED = "canceled"


class SubscriptionBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Netflix"})
    amount: float = Field(..., gt=0, json_schema_extra={"example": 12.99})
    billing_cycle: BillingCycle = Field(default=BillingCycle.MONTHLY)
    next_billing_date: date = Field(..., json_schema_extra={"example": "2026-11-01"})
    status: SubscriptionStatus = Field(default=SubscriptionStatus.ACTIVE)


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    amount: Optional[float] = Field(None, gt=0)
    billing_cycle: Optional[BillingCycle] = None
    next_billing_date: Optional[date] = None
    status: Optional[SubscriptionStatus] = None


class SubscriptionResponse(SubscriptionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int