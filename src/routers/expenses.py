import csv
import io
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.expense import ExpenseModel
from src.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate, ExpenseCategory

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)



@router.get("/", response_model=List[ExpenseResponse])
def get_all_expenses(
    category: Optional[ExpenseCategory] = Query(None, description="Φιλτράρισμα ανά κατηγορία"),
    start_date: Optional[date] = Query(None, description="Έξοδα από αυτή την ημερομηνία"),
    end_date: Optional[date] = Query(None, description="Έξοδα έως αυτή την ημερομηνία"),
    skip: int = Query(0, ge=0, description="Αριθμός εγγραφών προς παράλειψη (pagination)"),
    limit: int = Query(20, ge=1, le=100, description="Μέγιστος αριθμός αποτελεσμάτων"),
    db: Session = Depends(get_db)
):
    query = db.query(ExpenseModel)

    if category:
        query = query.filter(ExpenseModel.category == category.value)
    if start_date:
        query = query.filter(ExpenseModel.expense_date >= start_date)
    if end_date:
        query = query.filter(ExpenseModel.expense_date <= end_date)

    expenses = query.offset(skip).limit(limit).all()
    return expenses



@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = ExpenseModel(
        title=expense.title,
        amount=expense.amount,
        category=expense.category.value,
        expense_date=expense.expense_date,
        notes=expense.notes
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.get("/export", response_class=StreamingResponse)
def export_expenses_to_csv(
    category: Optional[ExpenseCategory] = Query(None, description="Φιλτράρισμα ανά κατηγορία"),
    start_date: Optional[date] = Query(None, description="Έξοδα από αυτή την ημερομηνία"),
    end_date: Optional[date] = Query(None, description="Έξοδα έως αυτή την ημερομηνία"),
    db: Session = Depends(get_db)
):
    query = db.query(ExpenseModel)

    if category:
        query = query.filter(ExpenseModel.category == category.value)
    if start_date:
        query = query.filter(ExpenseModel.expense_date >= start_date)
    if end_date:
        query = query.filter(ExpenseModel.expense_date <= end_date)

    expenses = query.order_by(ExpenseModel.expense_date.desc()).all()

    
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["ID", "Title", "Amount (€)", "Category", "Date", "Notes"])

   
    for exp in expenses:
        writer.writerow([
            exp.id,
            exp.title,
            exp.amount,
            exp.category,
            exp.expense_date.strftime("%Y-%m-%d") if exp.expense_date else "",
            exp.notes or ""
        ])

    output.seek(0)

    
    headers = {
        "Content-Disposition": "attachment; filename=expenses_export.csv",
        "Content-Type": "text/csv; charset=utf-8"
    }

    return StreamingResponse(iter([output.getvalue()]), headers=headers, media_type="text/csv")

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense_by_id(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found"
        )
    return expense



@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense_update: ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found"
        )

    update_data = expense_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "category" and value is not None:
            setattr(db_expense, key, value.value)
        else:
            setattr(db_expense, key, value)

    db.commit()
    db.refresh(db_expense)
    return db_expense



@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not db_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found"
        )

    db.delete(db_expense)
    db.commit()
    return None