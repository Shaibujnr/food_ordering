from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from foodie import util
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
