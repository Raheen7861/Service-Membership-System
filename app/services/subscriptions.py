from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from .. import models


def get_active_subscription_for_member(
    db: Session,
    member_id: int,
    today: Optional[date] = None,
) -> Optional[models.Subscription]:

    if today is None:
        today = date.today()

    return (
        db.query(models.Subscription)
        .filter(
            models.Subscription.member_id == member_id,
            models.Subscription.start_date <= today,
            models.Subscription.end_date >= today,
        )
        .order_by(models.Subscription.start_date.desc())
        .first()
    )
