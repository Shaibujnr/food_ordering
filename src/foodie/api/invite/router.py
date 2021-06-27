from uuid import UUID
from jwt import PyJWTError
from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
from sqlalchemy.orm.session import Session
from foodie import enums, util
from foodie.api import deps, exceptions
from .schema import InviteTokenDetailsSchema, AcceptInviteSchema
from foodie.dataclasses import InvitationTokenPayload
from foodie.db import models


router = APIRouter()


@router.post("/details", response_model=InviteTokenDetailsSchema)
def get_invitation_token_details(
    token: str, session: Session = Depends(deps.get_session)
):
    """
    Get details of an invitation token
    """
    try:
        token_payload = util.get_payload_from_token(token)
        token_payload: InvitationTokenPayload = InvitationTokenPayload(**token_payload)
        if token_payload.token_type == enums.ActivityTokenType.VENDOR_ADMIN_INVITE:
            vendor_id = UUID(token_payload.id)
            vendor_admin_email = token_payload.email
            vendor: models.Vendor = session.query(models.Vendor).get(vendor_id)
            if vendor is None:
                raise exceptions.invalid_or_expired_token_exception
            existing_vendor_user = (
                session.query(models.VendorUser)
                .filter(models.VendorUser.vendor_id == vendor.id)
                .filter(models.VendorUser.email == vendor_admin_email)
                .one_or_none()
            )
            if existing_vendor_user is not None:
                raise exceptions.invalid_or_expired_token_exception
            return {
                "email": vendor_admin_email,
                "role": "admin",
                "user_type": "vendor",
                "name": vendor.name,
            }
        elif token_payload.token_type == enums.ActivityTokenType.COURIER_ADMIN_INVITE:
            courier_id = UUID(token_payload.id)
            courier_admin_email = token_payload.email
            courier: models.Courier = session.query(models.Courier).get(courier_id)
            if courier is None:
                raise exceptions.invalid_or_expired_token_exception
            existing_courier_user = (
                session.query(models.CourierUser)
                .filter(models.CourierUser.courier_id == courier_id)
                .filter(models.CourierUser.email == courier_admin_email)
                .one_or_none()
            )
            if existing_courier_user is not None:
                raise exceptions.invalid_or_expired_token_exception
            return {
                "email": courier_admin_email,
                "role": "admin",
                "user_type": "courier",
                "name": courier.name,
            }
        elif token_payload.token_type == enums.ActivityTokenType.VENDOR_USER_INVITE:
            vendor_id = UUID(token_payload.id)
            vendor_user_email = token_payload.email
            vendor: models.Vendor = session.query(models.Vendor).get(vendor_id)
            if vendor is None:
                raise exceptions.invalid_or_expired_token_exception
            existing_vendor_user = (
                session.query(models.VendorUser)
                .filter(models.VendorUser.vendor_id == vendor.id)
                .filter(models.VendorUser.email == vendor_user_email)
                .one_or_none()
            )
            if existing_vendor_user is not None:
                raise exceptions.invalid_or_expired_token_exception
            return {
                "email": vendor_user_email,
                "role": "staff",
                "user_type": "vendor",
                "name": vendor.name,
            }
        elif token_payload.token_type == enums.ActivityTokenType.COURIER_USER_INVITE:
            courier_id = UUID(token_payload.id)
            courier_user_email = token_payload.email
            courier: models.Courier = session.query(models.Courier).get(courier_id)
            if courier is None:
                raise exceptions.invalid_or_expired_token_exception
            existing_courier_user = (
                session.query(models.CourierUser)
                .filter(models.CourierUser.courier_id == courier_id)
                .filter(models.CourierUser.email == courier_user_email)
                .one_or_none()
            )
            if existing_courier_user is not None:
                raise exceptions.invalid_or_expired_token_exception
            return {
                "email": courier_user_email,
                "role": "staff",
                "user_type": "courier",
                "name": courier.name,
            }
        else:
            raise HTTPException(400, "Invalid token")
    except ValidationError:
        raise exceptions.invalid_or_expired_token_exception
    except PyJWTError:
        raise exceptions.invalid_or_expired_token_exception


@router.post("/accept")
def accept_admin_invitation(
    token: str,
    payload: AcceptInviteSchema,
    session: Session = Depends(deps.get_session),
):
    """
    Accept invitation from platform admin to be an admin user for a particular vendor
    """
    try:
        token_payload = util.get_payload_from_token(token)
        token_payload: InvitationTokenPayload = InvitationTokenPayload(**token_payload)
        if token_payload.token_type == enums.ActivityTokenType.VENDOR_ADMIN_INVITE:
            vendor_id = UUID(token_payload.id)
            vendor_admin_email = token_payload.email
            vendor: models.Vendor = session.query(models.Vendor).get(vendor_id)
            if vendor is None:
                raise exceptions.invalid_or_expired_token_exception
            existing_vendor_user = (
                session.query(models.VendorUser)
                .filter(models.VendorUser.vendor_id == vendor.id)
                .filter(models.VendorUser.email == vendor_admin_email)
                .one_or_none()
            )
            if existing_vendor_user is not None:
                raise exceptions.invalid_or_expired_token_exception
            vendor_admin: models.VendorUser = models.VendorUser(
                vendor_id=vendor.id,
                first_name=payload.first_name,
                last_name=payload.last_name,
                phone_number=payload.phone_number,
                email=vendor_admin_email,
                role=enums.VendorUserRole.ADMIN,
                hashed_password=util.hash_password(payload.password),
            )
            session.add(vendor_admin)
        elif token_payload.token_type == enums.ActivityTokenType.COURIER_ADMIN_INVITE:
            courier_id = UUID(token_payload.id)
            courier_admin_email = token_payload.email
            courier: models.Courier = session.query(models.Courier).get(courier_id)
            if courier is None:
                raise exceptions.invalid_or_expired_token_exception
            existing_courier_user = (
                session.query(models.CourierUser)
                .filter(models.CourierUser.courier_id == courier_id)
                .filter(models.CourierUser.email == courier_admin_email)
                .one_or_none()
            )
            if existing_courier_user is not None:
                raise exceptions.invalid_or_expired_token_exception
            courier_admin: models.CourierUser = models.CourierUser(
                courier_id=courier.id,
                first_name=payload.first_name,
                last_name=payload.last_name,
                phone_number=payload.phone_number,
                email=courier_admin_email,
                role=enums.VendorUserRole.ADMIN,
                hashed_password=util.hash_password(payload.password),
            )
            session.add(courier_admin)
        elif token_payload.token_type == enums.ActivityTokenType.VENDOR_USER_INVITE:
            vendor_id = UUID(token_payload.id)
            vendor_user_email = token_payload.email
            vendor: models.Vendor = session.query(models.Vendor).get(vendor_id)
            if vendor is None:
                raise exceptions.invalid_or_expired_token_exception
            existing_vendor_user = (
                session.query(models.VendorUser)
                .filter(models.VendorUser.vendor_id == vendor.id)
                .filter(models.VendorUser.email == vendor_user_email)
                .one_or_none()
            )
            if existing_vendor_user is not None:
                raise exceptions.invalid_or_expired_token_exception
            vendor_user: models.VendorUser = models.VendorUser(
                vendor_id=vendor.id,
                first_name=payload.first_name,
                last_name=payload.last_name,
                phone_number=payload.phone_number,
                email=vendor_user_email,
                role=enums.VendorUserRole.STAFF,
                hashed_password=util.hash_password(payload.password),
            )
            session.add(vendor_user)
        elif token_payload.token_type == enums.ActivityTokenType.COURIER_USER_INVITE:
            courier_id = UUID(token_payload.id)
            courier_user_email = token_payload.email
            courier: models.Courier = session.query(models.Courier).get(courier_id)
            if courier is None:
                raise exceptions.invalid_or_expired_token_exception
            existing_courier_user = (
                session.query(models.CourierUser)
                .filter(models.CourierUser.courier_id == courier_id)
                .filter(models.CourierUser.email == courier_user_email)
                .one_or_none()
            )
            if existing_courier_user is not None:
                raise exceptions.invalid_or_expired_token_exception
            courier_user: models.CourierUser = models.CourierUser(
                courier_id=courier.id,
                first_name=payload.first_name,
                last_name=payload.last_name,
                phone_number=payload.phone_number,
                email=courier_user_email,
                role=enums.VendorUserRole.STAFF,
                hashed_password=util.hash_password(payload.password),
            )
            session.add(courier_user)
        else:
            raise HTTPException(400, "Invalid token")
        session.commit()
    except ValidationError:
        raise exceptions.invalid_or_expired_token_exception
    except PyJWTError:
        raise exceptions.invalid_or_expired_token_exception
