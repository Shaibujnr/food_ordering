from foodie.api.schema import BaseSchema, OrmSchema


class CourierCreateSchema(BaseSchema):
    name: str
    address: str


class CourierSchema(OrmSchema, CourierCreateSchema):
    pass
