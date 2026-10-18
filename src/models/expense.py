from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date
from src.database import Base


class ExpenseModel(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False, default="other")
    expense_date = Column(Date, default=date.today)
    notes = Column(String(255), nullable=True)