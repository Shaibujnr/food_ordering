from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from pydantic.networks import EmailStr
from sqlalchemy.orm.session import Session
from foodie import config, enums, util
from foodie.api import deps
from foodie.db import models


router = APIRouter()


@router.post("/")
def invite_courier_user(
    email: EmailStr,
    courier_admin: models.CourierUser = Depends(deps.get_current_courier_admin),
    session: Session = Depends(deps.get_session),
):
    courier: models.Courier = courier_admin.courier
    existing_courier_user_with_same_email = (
        session.query(models.CourierUser)
        .filter(models.CourierUser.courier_id == courier.id)
        .filter(models.CourierUser.email == email)
        .one_or_none()
    )
    if existing_courier_user_with_same_email:
        raise HTTPException(400, "Courier user with same email exists")
    invite_token = util.create_token(
        {
            "courier_id": str(courier.id),
            "email": email,
            "token_type": enums.ActivityTokenType.COURIER_USER_INVITE,
        },
        config.ACTIVITY_TOKEN_SECRET_KEY,
        timedelta(hours=1),
    )
    print("\n\n\n\n\n")
    print(f"courier user invite token is: {invite_token}")
    print("\n\n\n\n\n\n")
