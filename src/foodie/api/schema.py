import inflection
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class BaseSchema(BaseModel):
    class Config:
        extra = "forbid"
        alias_generator = lambda x: inflection.camelize(x, False)  # noqa
        allow_population_by_field_name = True


class BaseOrmSchema(BaseSchema):
    class Config:
        orm_mode = True


class OrmWithIdSchema(BaseOrmSchema):
    id: UUID


class OrmWithDateTimeSchema(BaseOrmSchema):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OrmSchema(OrmWithDateTimeSchema, OrmWithIdSchema):
    pass


class BasePaginationSchema(BaseSchema):
    page: int
    page_size: int
    count: int
