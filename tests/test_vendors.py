from datetime import time
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session
from foodie import enums
from foodie.db import models


def test_fetch_vendors(
    client: TestClient,
    session: Session,
    home_vendor,
    restaurant_vendor,
    food_stand_vendor,
):
    # Assert open information returned
    assert session.query(models.Vendor).count() == 3
    response = client.get("/api/vendors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    data = response.json()
    assert len(data) == 3
    sample_vendor_response = data[0]
    assert "openInformations" in sample_vendor_response
    assert isinstance(sample_vendor_response["openInformations"], list)
    assert len(sample_vendor_response["openInformations"]) == 7
    assert isinstance(sample_vendor_response["openInformations"][0], dict)


def test_update_vendor_open_information(
    client: TestClient,
    session: Session,
    home_vendor: models.Vendor,
    home_vendor_admin_auth_header: dict,
):
    assert len(home_vendor.open_informations) == 7
    monday_open_information = (
        session.query(models.OpenInformation)
        .filter(models.OpenInformation.vendor_id == home_vendor.id)
        .filter(models.OpenInformation.day == enums.DaysOfTheWeek.MONDAY)
        .one()
    )
    assert monday_open_information.is_closed
    assert monday_open_information.open_from == time(9, 0, 0)
    assert monday_open_information.open_to == time(19, 0, 0)
    response = client.put(
        f"/api/vendor-admin/open-informations/{enums.DaysOfTheWeek.MONDAY}",
        json={"is_closed": False, "open_from": "10:00:00"},
        headers=home_vendor_admin_auth_header,
    )
    session.expire_all()
    assert response.status_code == 200
    assert not monday_open_information.is_closed
    assert monday_open_information.open_from == time(10, 0, 0)
    assert monday_open_information.open_to == time(19, 0, 0)


def test_update_vendor_open_information_with_open_from_time_greater_than_open_to_time_fail(
    client: TestClient,
    session: Session,
    home_vendor: models.Vendor,
    home_vendor_admin_auth_header: dict,
):
    assert len(home_vendor.open_informations) == 7
    monday_open_information = (
        session.query(models.OpenInformation)
        .filter(models.OpenInformation.vendor_id == home_vendor.id)
        .filter(models.OpenInformation.day == enums.DaysOfTheWeek.MONDAY)
        .one()
    )
    assert monday_open_information.is_closed
    assert monday_open_information.open_from == time(9, 0, 0)
    assert monday_open_information.open_to == time(19, 0, 0)
    response = client.put(
        f"/api/vendor-admin/open-informations/{enums.DaysOfTheWeek.MONDAY}",
        json={"is_closed": False, "open_from": "22:00:00", "open_to": "09:00:00"},
        headers=home_vendor_admin_auth_header,
    )
    assert response.status_code == 422
