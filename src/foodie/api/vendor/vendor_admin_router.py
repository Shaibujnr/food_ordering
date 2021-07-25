from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from foodie.api import deps
from foodie import enums
from foodie.db import models
from .schema import OpenInformationUpdateSchema, VendorSchema


router = APIRouter()


@router.put("/open-informations/{day}", response_model=VendorSchema, status_code=200)
def update_vendor_open_information(
    day: enums.DaysOfTheWeek,
    payload: OpenInformationUpdateSchema,
    vendor_admin: models.VendorUser = Depends(deps.get_current_vendor_admin),
    session: Session = Depends(deps.get_session),
):
    vendor: models.Vendor = vendor_admin.vendor
    open_information = (
        session.query(models.OpenInformation)
        .filter(models.OpenInformation.vendor_id == vendor.id)
        .filter(models.OpenInformation.day == day)
        .one()
    )
    update_data = payload.dict(exclude_unset=True)
    for key, val in update_data.items():
        setattr(open_information, key, val)
    session.commit()
    return vendor


@router.get("/", response_model=List[VendorSchema])
def fetch_vendors(session: Session = Depends(deps.get_session)):
    return session.query(models.Vendor).all()
