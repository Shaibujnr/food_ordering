from typing import Literal
from pydantic import validator
from pydantic.networks import EmailStr
from foodie.api.schema import BaseSchema


class AcceptInviteSchema(BaseSchema):
    first_name: str
    last_name: str
    phone_number: str
    password: str

    @validator("password")
    def validate_password(cls, password: str):
        assert len(password.strip()) >= 6
        return password


class InviteTokenDetailsSchema(BaseSchema):
    email: EmailStr
    user_type: Literal["vendor", "courier"]
    role: Literal["admin", "staff", "manager"]
    name: str
