from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..services.subscriptions import get_active_subscription_for_member

router = APIRouter()


@router.post(
    "/check-in",
    response_model=schemas.AttendanceRead,
    status_code=status.HTTP_201_CREATED,
)
def check_in(
    payload: schemas.AttendanceCheckInRequest, db: Session = Depends(get_db)
):
    member = db.query(models.Member).filter(models.Member.id == payload.member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found."
        )

    active_sub = get_active_subscription_for_member(db, payload.member_id)
    if not active_sub:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active subscription for this member.",
        )

    attendance = models.Attendance(member_id=payload.member_id)
    db.add(attendance)
    db.commit()
    db.refresh(attendance)


    return attendance


@router.get("/members/{member_id}", response_model=schemas.AttendanceList)
def get_member_attendance(member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found."
        )

    records = (
        db.query(models.Attendance)
        .filter(models.Attendance.member_id == member_id)
        .order_by(models.Attendance.check_in_time.desc())
        .all()
    )

    return schemas.AttendanceList(member_id=member_id, records=records)
