from uuid import UUID
from fastapi import Depends, HTTPException
from fastapi import status as status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from foodie import enums, util
from foodie.db import models
from foodie.db.base import SessionLocal


user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth")
admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/auth")
vendor_admin_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/vendor-admin/auth"
)  # noqa
courier_admin_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/courier-admin/auth"
)  # noqa
vendor_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/vendor/auth")
courier_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/courier/auth")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_session() -> Session:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_current_user(
    token: bytes = Depends(user_oauth2_scheme),
    session: Session = Depends(get_session),
) -> models.User:
    user_id: str = util.decode_access_token(token)
    user: models.User = session.query(models.User).get(UUID(user_id))
    if not user:
        raise credentials_exception
    return user


def get_current_admin(
    token: bytes = Depends(admin_oauth2_scheme),
    session: Session = Depends(get_session),
) -> models.Admin:
    admin_id: str = util.decode_access_token(token)
    admin: models.Admin = session.query(models.Admin).get(UUID(admin_id))
    if not admin:
        raise credentials_exception
    return admin


def get_current_vendor_admin(
    token: bytes = Depends(vendor_admin_oauth2_scheme),
    session: Session = Depends(get_session),
) -> models.VendorUser:
    vendor_admin_id: str = util.decode_access_token(token)
    vendor_admin: models.VendorUser = (
        session.query(models.VendorUser)
        .filter(models.VendorUser.id == UUID(vendor_admin_id))
        .filter(models.VendorUser.role == enums.VendorUserRole.ADMIN)
        .one_or_none()
    )
    if vendor_admin is None:
        raise credentials_exception
    return vendor_admin


def get_current_courier_admin(
    token: bytes = Depends(courier_admin_oauth2_scheme),
    session: Session = Depends(get_session),
) -> models.CourierUser:
    courier_admin_id: str = util.decode_access_token(token)
    courier_admin: models.CourierUser = (
        session.query(models.CourierUser)
        .filter(models.CourierUser.id == UUID(courier_admin_id))
        .filter(models.CourierUser.role == enums.CourierUserRole.ADMIN)
        .one_or_none()
    )
    if courier_admin is None:
        raise credentials_exception
    return courier_admin


def get_current_vendor(
    token: bytes = Depends(vendor_oauth2_scheme),
    session: Session = Depends(get_session),
) -> models.VendorUser:
    vendor_id: str = util.decode_access_token(token)
    vendor: models.VendorUser = session.query(models.VendorUser).get(
        UUID(vendor_id)
    )  # noqa
    if vendor is None:
        raise credentials_exception
    return vendor


def get_current_courier(
    token: bytes = Depends(courier_oauth2_scheme),
    session: Session = Depends(get_session),
) -> models.CourierUser:
    courier_id: str = util.decode_access_token(token)
    courier: models.CourierUser = session.query(models.CourierUser).get(
        UUID(courier_id)
    )
    if courier is None:
        raise credentials_exception
    return courier
