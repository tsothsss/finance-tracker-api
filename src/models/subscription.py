from sqlalchemy import Column, Integer, String, Float, Date
from src.database import Base


class SubscriptionModel(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    billing_cycle = Column(String(20), nullable=False, default="monthly")
    next_billing_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="active")