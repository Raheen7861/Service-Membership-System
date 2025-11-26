from fastapi import APIRouter

from . import members, plans, subscriptions, attendance

api_router = APIRouter()

api_router.include_router(members.router, prefix="/members", tags=["members"])
api_router.include_router(plans.router, prefix="/plans", tags=["plans"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
