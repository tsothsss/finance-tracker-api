from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.subscription import SubscriptionModel
from src.schemas.subscription import SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


@router.get("/", response_model=List[SubscriptionResponse])
def get_all_subscriptions(db: Session = Depends(get_db)):
    return db.query(SubscriptionModel).all()


@router.post("/", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
def create_subscription(sub: SubscriptionCreate, db: Session = Depends(get_db)):
    db_sub = SubscriptionModel(
        name=sub.name,
        amount=sub.amount,
        billing_cycle=sub.billing_cycle.value,
        next_billing_date=sub.next_billing_date,
        status=sub.status.value
    )
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub


@router.delete("/{sub_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscription(sub_id: int, db: Session = Depends(get_db)):
    sub = db.query(SubscriptionModel).filter(SubscriptionModel.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    db.delete(sub)
    db.commit()
    return None