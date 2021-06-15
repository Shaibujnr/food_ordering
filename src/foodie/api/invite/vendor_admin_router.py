from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from pydantic.networks import EmailStr
from sqlalchemy.orm.session import Session
from foodie import config, enums, util
from foodie.api import deps
from foodie.db import models


router = APIRouter()


@router.post("/")
def invite_vendor_user(
    email: EmailStr,
    vendor_admin: models.VendorUser = Depends(deps.get_current_vendor_admin),
    session: Session = Depends(deps.get_session),
):
    vendor: models.Vendor = vendor_admin.vendor
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
            "token_type": enums.ActivityTokenType.VENDOR_USER_INVITE,
        },
        config.ACTIVITY_TOKEN_SECRET_KEY,
        timedelta(hours=1),
    )
    print("\n\n\n\n\n")
    print(f"vendor user invite token is: {invite_token}")
    print("\n\n\n\n\n\n")
