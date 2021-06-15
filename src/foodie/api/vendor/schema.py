from foodie.api.schema import BaseSchema, OrmSchema
from foodie import enums


class VendorCreateSchema(BaseSchema):
    name: str
    type: enums.VendorType
    address: str


class VendorSchema(OrmSchema, VendorCreateSchema):
    pass
