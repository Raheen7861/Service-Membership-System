from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..database import get_db
from .. import models, schemas

router = APIRouter()


@router.post("", response_model=schemas.PlanRead, status_code=status.HTTP_201_CREATED)
def create_plan(plan_in: schemas.PlanCreate, db: Session = Depends(get_db)):
    plan = models.Plan(
        name=plan_in.name,
        price=plan_in.price,
        duration_days=plan_in.duration_days,
    )
    db.add(plan)
    try:
        db.commit()
        db.refresh(plan)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A plan with this name already exists.",
        )
    return plan


@router.get("", response_model=List[schemas.PlanRead])
def list_plans(db: Session = Depends(get_db)):
    return db.query(models.Plan).order_by(models.Plan.id.asc()).all()
