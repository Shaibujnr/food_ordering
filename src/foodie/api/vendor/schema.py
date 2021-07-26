from typing import List, Optional
from pydantic import root_validator
from datetime import time
from foodie.api.schema import BaseSchema, OrmSchema
from foodie import enums


class OpenInformationUpdateSchema(BaseSchema):
    is_closed: Optional[bool]
    closed_reason: Optional[str]
    open_from: Optional[time]
    open_to: Optional[time]

    @root_validator
    def validate_open_period(cls, data):
        open_from = data["open_from"]
        open_to = data["open_to"]
        if open_from is not None and open_to is not None:
            assert open_from < open_to
        return data


class OpenInformationSchema(OrmSchema, OpenInformationUpdateSchema):
    day: enums.DaysOfTheWeek


class VendorCreateSchema(BaseSchema):
    name: str
    type: enums.VendorType
    address: str


class VendorSchema(OrmSchema, VendorCreateSchema):
    open_informations: List[OpenInformationSchema]
