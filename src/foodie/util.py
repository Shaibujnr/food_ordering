import jwt
from typing import Any, Union
from datetime import datetime, timedelta
from passlib.context import CryptContext
from foodie import config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(payload: dict, secret: str, expires_delta: timedelta):
    to_encode = payload.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=config.JWT_ALGORITHM)  # noqa


def create_access_token(
    data: dict, secret=config.SECRET_KEY, expires_delta: timedelta = None
):
    expire = expires_delta or timedelta(seconds=config.ACCESS_TOKEN_EXPIRE)
    return create_token(data, secret, expire)


def get_payload_from_token(token: Union[str, bytes], secret) -> Any:
    return jwt.decode(token, secret, algorithms=[config.JWT_ALGORITHM])  # noqa


def decode_access_token(token: Union[str, bytes], secret=config.SECRET_KEY) -> str:
    # scenario token is not valid
    payload = get_payload_from_token(token, secret)
    user_id: str = payload.get("sub")  # type: ignore
    return user_id


def password_is_match(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str):
    return pwd_context.hash(plain_password)


# def send_email(
#     to: str,
#     subject: str,
#     message: str,
#     html: Optional[str] = None,
# ):
#     """
#     Send out email with sendgrid
#     """
#     try:
#         msg = Mail(
#             from_email="noreply@digirent.com",
#             to_emails=to,
#             subject=subject,
#             plain_text_content=message,
#             html_content=html,
#         )
#         if not config.IS_TEST:
#             print("\n\n\n\n")
#             print(str(message))
#             print("\n\n\n\n")
#         sg = SendGridAPIClient(config.SENDGRID_API_KEY)
#         sg.send(msg)
#     except Exception as e:
#         print("\n\n\n\n")
#         print("Sendgrid failed")
#         print(str(e))
#         print("\n\n\n\n")
