from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from foodie import util, enums
from foodie.api import deps, exceptions
from foodie.db import models
from .schema import TokenSchema


router = APIRouter()


@router.post("/auth", response_model=TokenSchema)
def authenticate(
    data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(deps.get_session),
):
    user: models.User = (
        session.query(models.User)
        .filter(models.User.email == data.username)
        .one_or_none()
    )
    if not user:
        raise exceptions.invalid_login_credentials_exception
    if not util.password_is_match(data.password, user.hashed_password):
        raise exceptions.invalid_login_credentials_exception
    access_token = util.create_access_token({"sub": str(user.id)})
    return TokenSchema(access_token=access_token)


@router.post("/auth/admin", response_model=TokenSchema)
def authenticate_admin(
    data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(deps.get_session),
):
    admin: models.Admin = (
        session.query(models.Admin)
        .filter(models.Admin.email == data.username)
        .one_or_none()
    )
    if not admin:
        raise exceptions.invalid_login_credentials_exception
    if not util.password_is_match(data.password, admin.hashed_password):
        raise exceptions.invalid_login_credentials_exception
    access_token = util.create_access_token({"sub": str(admin.id)})
    return TokenSchema(access_token=access_token)


@router.post("/auth/courier", response_model=TokenSchema)
def authenticate_courier(
    data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(deps.get_session),
):
    user: models.CourierUser = (
        session.query(models.CourierUser)
        .filter(models.CourierUser.email == data.username)
        .filter(models.CourierUser.role == enums.CourierUserRole.ADMIN)
        .one_or_none()
    )
    if not user:
        raise exceptions.invalid_login_credentials_exception
    if not util.password_is_match(data.password, user.hashed_password):
        raise exceptions.invalid_login_credentials_exception
    access_token = util.create_access_token({"sub": str(user.id)})
    return TokenSchema(access_token=access_token)


@router.post("/auth/vendor", response_model=TokenSchema)
def authenticate_vendor(
    data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(deps.get_session),
):
    user: models.VendorUser = (
        session.query(models.VendorUser)
        .filter(models.VendorUser.email == data.username)
        .one_or_none()
    )
    if not user:
        raise exceptions.invalid_login_credentials_exception
    if not util.password_is_match(data.password, user.hashed_password):
        raise exceptions.invalid_login_credentials_exception
    access_token = util.create_access_token({"sub": str(user.id)})
    return TokenSchema(access_token=access_token)


@router.post("/auth/courier-admin", response_model=TokenSchema)
def authenticate_courier_admin(
    data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(deps.get_session),
):
    user: models.CourierUser = (
        session.query(models.CourierUser)
        .filter(models.CourierUser.email == data.username)
        .filter(models.CourierUser.role == enums.CourierUserRole.ADMIN)
        .one_or_none()
    )
    if not user:
        raise exceptions.invalid_login_credentials_exception
    if not util.password_is_match(data.password, user.hashed_password):
        raise exceptions.invalid_login_credentials_exception
    access_token = util.create_access_token({"sub": str(user.id)})
    return TokenSchema(access_token=access_token)


@router.post("/auth/vendor-admin", response_model=TokenSchema)
def authenticate_vendor_admin(
    data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(deps.get_session),
):
    user: models.VendorUser = (
        session.query(models.VendorUser)
        .filter(models.VendorUser.email == data.username)
        .filter(models.VendorUser.role == enums.VendorUserRole.ADMIN)
        .one_or_none()
    )
    if not user:
        raise exceptions.invalid_login_credentials_exception
    if not util.password_is_match(data.password, user.hashed_password):
        raise exceptions.invalid_login_credentials_exception
    access_token = util.create_access_token({"sub": str(user.id)})
    return TokenSchema(access_token=access_token)
