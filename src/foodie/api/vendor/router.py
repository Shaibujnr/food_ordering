from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from foodie.api import deps
from foodie.db import models
from .schema import VendorSchema


router = APIRouter()


@router.get("/", response_model=List[VendorSchema])
def fetch_vendors(session: Session = Depends(deps.get_session)):
    return session.query(models.Vendor).all()
