from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..database import get_db
from .. import models, schemas
from ..services.subscriptions import get_active_subscription_for_member

router = APIRouter()


@router.post(
    "",
    response_model=schemas.MemberRead,
    status_code=status.HTTP_201_CREATED,
)
def create_member(
    member_in: schemas.MemberCreate,
    db: Session = Depends(get_db),
):

    member = models.Member(
        name=member_in.name,
        phone=member_in.phone,
        status=member_in.status,
    )
    db.add(member)
    try:
        db.commit()
        db.refresh(member)
    except IntegrityError:
        db.rollback()
        # Most likely phone uniqueness violation
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already exists for another member.",
        )
    return member


@router.get("", response_model=List[schemas.MemberRead])
def list_members(
    status: Optional[models.MemberStatus] = None,
    db: Session = Depends(get_db),
):

    query = db.query(models.Member)
    if status is not None:
        query = query.filter(models.Member.status == status)
    return query.order_by(models.Member.id.asc()).all()


