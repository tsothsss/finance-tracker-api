from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.database import get_db
from src.models.expense import ExpenseModel
from src.schemas.analytics import AnalyticsSummaryResponse

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/summary", response_model=AnalyticsSummaryResponse)
def get_expense_summary(
    start_date: Optional[date] = Query(None, description="Έναρξη περιόδου"),
    end_date: Optional[date] = Query(None, description="Λήξη περιόδου"),
    db: Session = Depends(get_db)
):
    query = db.query(ExpenseModel)

    if start_date:
        query = query.filter(ExpenseModel.expense_date >= start_date)
    if end_date:
        query = query.filter(ExpenseModel.expense_date <= end_date)

    total_count = query.count()
    if total_count == 0:
        return AnalyticsSummaryResponse(
            total_spent=0.0,
            total_expenses_count=0,
            average_expense_amount=0.0,
            by_category={}
        )

   
    total_spent_val = query.with_entities(func.sum(ExpenseModel.amount)).scalar() or 0.0

   
    category_rows = (
        query.with_entities(ExpenseModel.category, func.sum(ExpenseModel.amount))
        .group_by(ExpenseModel.category)
        .all()
    )
    by_category_dict = {cat: float(amt) for cat, amt in category_rows}

    avg_amt = round(total_spent_val / total_count, 2)

    return AnalyticsSummaryResponse(
        total_spent=round(float(total_spent_val), 2),
        total_expenses_count=total_count,
        average_expense_amount=avg_amt,
        by_category=by_category_dict
    )