from datetime import timedelta
from fastapi import APIRouter
from fastapi.param_functions import Depends
from pydantic.networks import EmailStr
from sqlalchemy.orm.session import Session
from starlette.exceptions import HTTPException
from foodie import config, enums, util
from foodie.api import deps
from foodie.db import models


router = APIRouter()


@router.post("/vendors/{vendor_id}")
def invite_vendor_admin(
    email: EmailStr,
    vendor: models.Vendor = Depends(deps.get_vendor),
    session: Session = Depends(deps.get_session),
):
    existing_vendor_user_with_same_email = (
        session.query(models.VendorUser)
        .filter(models.VendorUser.vendor_id == vendor.id)
        .filter(models.VendorUser.email == email)
        .one_or_none()
    )
    if existing_vendor_user_with_same_email:
        raise HTTPException(400, "Vendor user with same email exists")
    invite_token = util.create_token(
        {
            "vendor_id": str(vendor.id),
            "email": email,
            "token_type": enums.ActivityTokenType.VENDOR_ADMIN_INVITE,
        },
        config.ACTIVITY_TOKEN_SECRET_KEY,
        timedelta(hours=1),
    )
    print("\n\n\n\n\n")
    print(f"vendor admin invite token is: {invite_token}")
    print("\n\n\n\n\n\n")


@router.post("/couriers/{courier_id}")
def invite_courier_admin(
    email: EmailStr,
    courier: models.Courier = Depends(deps.get_courier),
    session: Session = Depends(deps.get_session),
):
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
            "token_type": enums.ActivityTokenType.COURIER_ADMIN_INVITE,
        },
        config.ACTIVITY_TOKEN_SECRET_KEY,
        timedelta(hours=1),
    )
    print("\n\n\n\n\n")
    print(f"courier admin invite token is: {invite_token}")
    print("\n\n\n\n\n\n")
