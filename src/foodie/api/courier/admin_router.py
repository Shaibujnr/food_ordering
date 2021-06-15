from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from starlette.exceptions import HTTPException
from foodie.api import deps
from foodie.db import models
from .schema import CourierSchema, CourierCreateSchema


router = APIRouter()


@router.post("/", response_model=CourierSchema)
def create_courier(
    payload: CourierCreateSchema, session: Session = Depends(deps.get_session)
):
    existing_courier = (
        session.query(models.Courier)
        .filter(models.Courier.name == payload.name)
        .one_or_none()
    )
    if existing_courier is not None:
        raise HTTPException(409, "Courier already exists")
    new_courier = models.Courier(**payload.dict(by_alias=False))
    session.add(new_courier)
    session.commit()
    return new_courier


@router.get("/", response_model=List[CourierSchema])
def fetch_couriers(session: Session = Depends(deps.get_session)):
    return session.query(models.Courier).all()
