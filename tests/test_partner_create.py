from datetime import time
from sqlalchemy.orm.session import Session
from fastapi.testclient import TestClient
from foodie.db import models
from foodie import enums


def test_create_vendor(admin_auth_header: dict, session: Session, client: TestClient):
    assert session.query(models.Vendor).count() == 0
    assert session.query(models.OpenInformation).count() == 0
    response = client.post(
        "/api/admin/vendors/",
        json={
            "name": "Vendor One Name",
            "type": enums.VendorType.RESTAURANT,
            "address": "vendor address",
        },
        headers=admin_auth_header,
    )
    assert response.status_code == 201
    assert session.query(models.Vendor).count() == 1
    vendor = session.query(models.Vendor).first()
    assert vendor.name == "Vendor One Name"
    assert vendor.address == "vendor address"
    assert vendor.type == enums.VendorType.RESTAURANT
    assert (
        session.query(models.OpenInformation)
        .filter(models.OpenInformation.vendor_id == vendor.id)
        .count()
        == 7
    )
    open_informations = (
        session.query(models.OpenInformation)
        .filter(models.OpenInformation.vendor_id == vendor.id)
        .all()
    )
    assert all(info.is_closed for info in open_informations)
    assert all(info.open_from == time(9, 0, 0) for info in open_informations)
    assert all(info.open_to == time(19, 0, 0) for info in open_informations)


def test_create_courier(admin_auth_header: dict, session: Session, client: TestClient):
    assert session.query(models.Courier).count() == 0
    response = client.post(
        "/api/admin/couriers/",
        json={
            "name": "Courier One Name",
            "address": "courier address",
        },
        headers=admin_auth_header,
    )
    assert response.status_code == 201
    assert session.query(models.Courier).count() == 1
    vendor = session.query(models.Courier).first()
    assert vendor.name == "Courier One Name"
    assert vendor.address == "courier address"
