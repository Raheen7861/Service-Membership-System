from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..database import get_db
from .. import models, schemas
from ..services.subscriptions import get_active_subscription_for_member

router = APIRouter()


@router.post("", response_model=schemas.SubscriptionRead, status_code=status.HTTP_201_CREATED)
def create_subscription(
    sub_in: schemas.SubscriptionCreate, db: Session = Depends(get_db)
):
    member = db.query(models.Member).filter(models.Member.id == sub_in.member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found."
        )

    plan = db.query(models.Plan).filter(models.Plan.id == sub_in.plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found."
        )
    

    existing = (
        db.query(models.Subscription)
        .filter(
            models.Subscription.member_id == sub_in.member_id,
            models.Subscription.plan_id == sub_in.plan_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This member is already subscribed to this plan.",
        )


    end_date = sub_in.start_date + timedelta(days=plan.duration_days)

    subscription = models.Subscription(
        member_id=sub_in.member_id,
        plan_id=sub_in.plan_id,
        start_date=sub_in.start_date,
        end_date=end_date,
    )
    db.add(subscription)

    try:
        db.commit()
        db.refresh(subscription)
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subscription for this member, plan and start date already exists.",
        )

    return subscription


@router.get("", response_model=List[schemas.SubscriptionRead])
def list_subscriptions(db: Session = Depends(get_db)):

    return (
        db.query(models.Subscription)
        .order_by(models.Subscription.id.asc())
        .all()
    )

@router.get(
    "/{member_id}/current-subscription",
    response_model=schemas.SubscriptionDetail,
)
def get_current_subscription_for_member(
    member_id: int,
    db: Session = Depends(get_db),
):


    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found.",
        )

    sub = get_active_subscription_for_member(db, member_id)

    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription for this member.",
        )

    return schemas.SubscriptionDetail(
        id=sub.id,
        member_id=sub.member_id,
        plan_id=sub.plan_id,
        plan_name=sub.plan.name,
        start_date=sub.start_date,
        end_date=sub.end_date,
    )

