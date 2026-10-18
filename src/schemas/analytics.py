from typing import Dict
from pydantic import BaseModel


class AnalyticsSummaryResponse(BaseModel):
    total_spent: float
    total_expenses_count: int
    average_expense_amount: float
    by_category: Dict[str, float]