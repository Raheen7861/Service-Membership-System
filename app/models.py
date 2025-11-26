from datetime import date, datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .database import Base
import enum


class MemberStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False, unique=True, index=True)
    join_date = Column(Date, nullable=False, default=date.today)
    status = Column(Enum(MemberStatus), nullable=False, default=MemberStatus.active)
    total_check_ins = Column(Integer, nullable=False, default=0)

    subscriptions = relationship(
        "Subscription", back_populates="member", cascade="all, delete-orphan"
    )
    attendance_records = relationship(
        "Attendance", back_populates="member", cascade="all, delete-orphan"
    )


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False)
    duration_days = Column(Integer, nullable=False)

    subscriptions = relationship(
        "Subscription", back_populates="plan", cascade="all, delete-orphan"
    )


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    __table_args__ = (
        UniqueConstraint("member_id", "plan_id", "start_date", name="uq_member_plan_start"),
    )

    member = relationship("Member", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")



class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    check_in_time = Column(
        DateTime, nullable=False, default=datetime.utcnow
    ) 

    member = relationship("Member", back_populates="attendance_records")
