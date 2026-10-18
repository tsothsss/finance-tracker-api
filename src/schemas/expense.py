from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ExpenseCategory(str, Enum):
    FOOD = "food"
    HOUSING = "housing"
    ENTERTAINMENT = "entertainment"
    TRANSPORT = "transport"
    UTILITIES = "utilities"
    SUBSCRIPTION = "subscription"
    OTHER = "other"


# Βασικά πεδία ελέγχου
class ExpenseBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Spotify Premium"})
    amount: float = Field(..., gt=0, json_schema_extra={"example": 7.99}, description="Amount must be positive")
    category: ExpenseCategory = Field(default=ExpenseCategory.OTHER)
    expense_date: date = Field(default_factory=date.today)
    notes: Optional[str] = Field(None, max_length=255, json_schema_extra={"example": "Monthly subscription"})



class ExpenseCreate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
   
class ExpenseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=100)
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[ExpenseCategory] = None
    expense_date: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=255)