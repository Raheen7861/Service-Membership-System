from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, constr, conint, condecimal

from .models import MemberStatus



class MemberBase(BaseModel):
    name:   constr(strip_whitespace=True, min_length=1)
    phone:  constr(strip_whitespace=True, min_length=5)
    status: Optional[MemberStatus] = MemberStatus.active
 

class MemberCreate(MemberBase):
    pass


class MemberRead(MemberBase):
    id: int
    join_date: date
    total_check_ins: int

    class Config:
        orm_mode = True




class PlanBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    price: condecimal(gt=0, max_digits=10, decimal_places=2)
    duration_days: conint(gt=0)


class PlanCreate(PlanBase):
    pass


class PlanRead(PlanBase):
    id: int

    class Config:
        orm_mode = True




class SubscriptionCreate(BaseModel):
    member_id: int
    plan_id: int
    start_date: date


class SubscriptionRead(BaseModel):
    id: int
    member_id: int
    plan_id: int
    start_date: date
    end_date: date

    class Config:
        orm_mode = True



class SubscriptionDetail(BaseModel):
    id: int
    member_id: int
    plan_id: int
    plan_name: str
    start_date: date
    end_date: date

    class Config:
        orm_mode = True



class AttendanceCheckInRequest(BaseModel):
    member_id: int


class AttendanceRead(BaseModel):
    id: int
    member_id: int
    check_in_time: datetime

    class Config:
        orm_mode = True


class AttendanceList(BaseModel):
    member_id: int
    records: List[AttendanceRead]
