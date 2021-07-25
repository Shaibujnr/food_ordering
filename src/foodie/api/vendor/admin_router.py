from typing import List
from datetime import time
from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from starlette.exceptions import HTTPException
from foodie import enums
from foodie.api import deps
from foodie.db import models
from .schema import VendorCreateSchema, VendorSchema


router = APIRouter()


@router.post("/", response_model=VendorSchema, status_code=201)
def create_vendor(
    payload: VendorCreateSchema, session: Session = Depends(deps.get_session)
):
    existing_vendor = (
        session.query(models.Vendor)
        .filter(models.Vendor.name == payload.name)
        .one_or_none()
    )
    if existing_vendor is not None:
        raise HTTPException(409, "Vendor already exists")
    new_vendor = models.Vendor(**payload.dict(by_alias=False))
    session.add(new_vendor)
    for day_of_the_week in enums.DaysOfTheWeek:
        open_information = models.OpenInformation(
            day=day_of_the_week,
            vendor=new_vendor,
            open_from=time(9, 0, 0),
            open_to=time(19, 0, 0),
            is_closed=True,
        )
        session.add(open_information)
    session.commit()
    return new_vendor


@router.get("/", response_model=List[VendorSchema])
def fetch_vendors(session: Session = Depends(deps.get_session)):
    return session.query(models.Vendor).all()
