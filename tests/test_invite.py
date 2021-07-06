import pytest
from datetime import timedelta
from sqlalchemy.orm.session import Session
from starlette.testclient import TestClient
from foodie.db import models
from foodie import util, enums, config


@pytest.fixture
def vendor_admin_invitation_token(restaurant_vendor: models.Vendor):
    return util.create_token(
        {
            "id": str(restaurant_vendor.id),
            "email": "vendor_admin@test.com",
            "token_type": enums.ActivityTokenType.VENDOR_ADMIN_INVITE,
        },
        config.ACTIVITY_TOKEN_SECRET_KEY,
        timedelta(hours=1),
    )


@pytest.fixture
def vendor_user_invitation_token(restaurant_vendor: models.Vendor):
    return util.create_token(
        {
            "id": str(restaurant_vendor.id),
            "email": "vendor_user@test.com",
            "token_type": enums.ActivityTokenType.VENDOR_USER_INVITE,
        },
        config.ACTIVITY_TOKEN_SECRET_KEY,
        timedelta(hours=1),
    )


@pytest.fixture
def courier_admin_invitation_token(courier: models.Courier):
    return util.create_token(
        {
            "id": str(courier.id),
            "email": "courier_admin@test.com",
            "token_type": enums.ActivityTokenType.COURIER_ADMIN_INVITE,
        },
        config.ACTIVITY_TOKEN_SECRET_KEY,
        timedelta(hours=1),
    )


@pytest.fixture
def courier_user_invitation_token(courier: models.Courier):
    return util.create_token(
        {
            "id": str(courier.id),
            "email": "courier_user@test.com",
            "token_type": enums.ActivityTokenType.COURIER_USER_INVITE,
        },
        config.ACTIVITY_TOKEN_SECRET_KEY,
        timedelta(hours=1),
    )


def test_admin_invite_vendor_admin(
    admin_auth_header: dict, vendor: models.Vendor, session: Session, client: TestClient
):
    assert session.query(models.Vendor).count() > 0
    response = client.post(
        f"/api/admin/invites/vendors/{vendor.id}",
        params={"email": "new_vendor_admin@test.com"},
        headers=admin_auth_header,
    )
    assert response.status_code == 200


def test_admin_invite_courier_admin(
    admin_auth_header: dict,
    courier: models.Courier,
    session: Session,
    client: TestClient,
):
    assert session.query(models.Courier).count() > 0
    response = client.post(
        f"/api/admin/invites/couriers/{courier.id}",
        params={"email": "new_courier_admin@test.com"},
        headers=admin_auth_header,
    )
    assert response.status_code == 200


def test_vendor_admin_invite_user(
    client: TestClient,
    sesssion: Session,
    restaurant_vendor_admin: models.VendorUser,
    restaurant_vendor_admin_auth_header: dict,
):
    assert (
        sesssion.query(models.VendorUser)
        .filter(models.VendorUser.vendor_id == restaurant_vendor_admin.id)
        .count()
        == 1
    )
    response = client.post(
        "/api/vendor-admin/invites",
        params={"email": "vendor_user@test.com"},
        headers=restaurant_vendor_admin_auth_header,
    )
    assert response.status_code == 200


def test_courier_admin_invite_user(
    client: TestClient,
    sesssion: Session,
    restaurant_vendor_admin: models.VendorUser,
    restaurant_vendor_admin_auth_header: dict,
):
    raise Exception()


def test_vendor_admin_accept_invite(
    vendor_admin_invitation_token: str,
    restaurant_vendor: models.Vendor,
    session: Session,
    client: TestClient,
):
    assert (
        session.query(models.VendorUser)
        .filter(models.VendorUser.vendor_id == restaurant_vendor.id)
        .count()
        == 0
    )
    response = client.post(
        "/api/invites/accept",
        json={
            "firstName": "John",
            "lastName": "Doe",
            "password": "xpassword",
            "phoneNumber": "08012345678",
        },
        params={"token": vendor_admin_invitation_token},
    )
    assert response.status_code == 201
    vendor_user = (
        session.query(models.VendorUser)
        .filter(models.VendorUser.vendor_id == restaurant_vendor.id)
        .first()
    )
    assert vendor_user is not None
    assert vendor_user.email == "vendor_admin@test.com"
    assert vendor_user.first_name == "John"
    assert vendor_user.last_name == "Doe"
    assert util.password_is_match("xpassword", vendor_user.hashed_password)
    assert vendor_user.phone_number == "08012345678"


def test_courier_admin_accept_invite(
    courier_admin_invitation_token: str,
    courier: models.Courier,
    session: Session,
    client: TestClient,
):
    assert (
        session.query(models.CourierUser)
        .filter(models.CourierUser.courier_id == courier.id)
        .count()
        == 0
    )
    response = client.post(
        "/api/invites/accept",
        json={
            "firstName": "John",
            "lastName": "Doe",
            "password": "xpassword",
            "phoneNumber": "08012345678",
        },
        params={"token": courier_admin_invitation_token},
    )
    assert response.status_code == 201
    courier_user = (
        session.query(models.CourierUser)
        .filter(models.CourierUser.courier_id == courier.id)
        .first()
    )
    assert courier_user is not None
    assert courier_user.email == "courier_admin@test.com"
    assert courier_user.first_name == "John"
    assert courier_user.last_name == "Doe"
    assert util.password_is_match("xpassword", courier_user.hashed_password)
    assert courier_user.phone_number == "08012345678"


def test_vendor_user_accept_invite():
    raise Exception()


def test_courier_user_accept_invite():
    raise Exception()


def test_accpet_invite_with_invalid_token_fail():
    raise Exception(0)


def test_invite_existing_user_fail():
    raise Exception()


def test_invite_user_to_non_existing_partner_platform():
    raise Exception()


def test_get_invitation_token_details(
    vendor_admin_invitation_token, courier_admin_invitation_token, client: TestClient
):
    response = client.get(
        "/api/invites/details",
        params={"token": vendor_admin_invitation_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "vendor_admin@test.com"
    assert data["userType"] == "vendor"
    assert data["role"] == "admin"
    assert data["name"] == "Restaurant Vendor"

    response = client.get(
        "/api/invites/details",
        params={"token": courier_admin_invitation_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "courier_admin@test.com"
    assert data["userType"] == "courier"
    assert data["role"] == "admin"
    assert data["name"] == "Courier Delivery"


def test_get_invitation_token_details_for_invalid_token_fail(client: TestClient):
    response = client.get(
        "/api/invites/details",
        params={"token": "invalid token"},
    )
    assert response.status_code == 400
    data = response.json()
    assert "Invalid" in data["detail"]
