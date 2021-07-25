import pytest
from foodie import enums
from tests.conftest import AdminDetails
from sqlalchemy.orm.session import Session
from starlette.testclient import TestClient
from foodie import util
from foodie.db import models


def test_authenticate_admin(
    client: TestClient,
    session: Session,
    admin: models.Admin,
    admin_details: AdminDetails,
):
    response = client.post(
        "/api/auth/admin",
        data={"username": admin_details.email, "password": admin_details.password},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "Bearer"


def test_authenticate_admin_with_invalid_credentials_fail(
    client: TestClient,
    session: Session,
    admin: models.Admin,
    admin_details: AdminDetails,
):
    assert admin_details.password != "wrongpassword"
    response = client.post(
        "/api/auth/admin",
        data={"username": admin_details.email, "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login credentials"


def test_authenticate_vendor_admin_on_vendor_platform(
    client: TestClient, home_vendor_admin: models.VendorUser
):
    assert home_vendor_admin.role == enums.VendorUserRole.ADMIN
    response = client.post(
        "/api/auth/vendor",
        data={"username": home_vendor_admin.email, "password": "password"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "Bearer"


def test_authenticate_vendor_admin_on_vendor_platform_with_wrong_credentials_fail(
    client: TestClient, home_vendor_admin: models.VendorUser
):
    assert home_vendor_admin.role == enums.VendorUserRole.ADMIN
    response = client.post(
        "/api/auth/vendor",
        data={"username": home_vendor_admin.email, "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login credentials"


def test_authenticate_vendor_admin_on_vendor_admin_platform(
    client: TestClient, home_vendor_admin: models.VendorUser
):
    assert home_vendor_admin.role == enums.VendorUserRole.ADMIN
    response = client.post(
        "/api/auth/vendor-admin",
        data={"username": home_vendor_admin.email, "password": "password"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "Bearer"


def test_authenticate_vendor_admin_on_vendor_admin_platform_with_wrong_credentials_fail(
    client: TestClient, home_vendor_admin: models.VendorUser
):
    assert home_vendor_admin.role == enums.VendorUserRole.ADMIN
    response = client.post(
        "/api/auth/vendor-admin",
        data={"username": home_vendor_admin.email, "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login credentials"


# Courier


def test_authenticate_courier_admin_on_courier_platform(
    client: TestClient, courier_admin: models.CourierUser
):
    assert courier_admin.role == enums.CourierUserRole.ADMIN
    response = client.post(
        "/api/auth/courier",
        data={"username": courier_admin.email, "password": "password"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "Bearer"


def test_authenticate_courier_admin_on_courier_platform_with_wrong_credentials_fail(
    client: TestClient, courier_admin: models.CourierUser
):
    assert courier_admin.role == enums.CourierUserRole.ADMIN
    response = client.post(
        "/api/auth/courier",
        data={"username": courier_admin.email, "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login credentials"


def test_authenticate_courier_admin_on_courier_admin_platform(
    client: TestClient, courier_admin: models.CourierUser
):
    assert courier_admin.role == enums.CourierUserRole.ADMIN
    response = client.post(
        "/api/auth/courier-admin",
        data={"username": courier_admin.email, "password": "password"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "Bearer"


def test_authenticate_courier_admin_on_courier_admin_platform_with_wrong_credentials_fail(
    client: TestClient, courier_admin: models.CourierUser
):
    assert courier_admin.role == enums.CourierUserRole.ADMIN
    response = client.post(
        "/api/auth/courier-admin",
        data={"username": courier_admin.email, "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login credentials"


@pytest.mark.parametrize(
    "non_admin_user",
    [
        pytest.lazy_fixture("home_vendor_admin"),
        pytest.lazy_fixture("courier_admin"),
        pytest.lazy_fixture("home_vendor_staff"),
        pytest.lazy_fixture("courier_staff"),
        pytest.lazy_fixture("user"),
    ],
)
def test_authenticate_non_admin_on_admin_platform_fail(client, non_admin_user):
    assert util.password_is_match("password", non_admin_user.hashed_password)
    response = client.post(
        "/api/auth/admin",
        data={"username": non_admin_user.email, "password": "password"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login credentials"


@pytest.mark.parametrize(
    "non_vendor_admin",
    [
        pytest.lazy_fixture("admin"),
        pytest.lazy_fixture("courier_admin"),
        pytest.lazy_fixture("home_vendor_staff"),
        pytest.lazy_fixture("courier_staff"),
        pytest.lazy_fixture("user"),
    ],
)
def test_authenticate_non_vendor_admin_on_vendor_admin_platform_fail(
    client, non_vendor_admin
):
    assert util.password_is_match("password", non_vendor_admin.hashed_password)
    response = client.post(
        "/api/auth/vendor-admin",
        data={"username": non_vendor_admin.email, "password": "password"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login credentials"


@pytest.mark.parametrize(
    "non_courier_admin",
    [
        pytest.lazy_fixture("home_vendor_admin"),
        pytest.lazy_fixture("admin"),
        pytest.lazy_fixture("home_vendor_staff"),
        pytest.lazy_fixture("courier_staff"),
        pytest.lazy_fixture("user"),
    ],
)
def test_authenticate_non_courier_admin_on_courier_admin_platform_fail(
    client, non_courier_admin
):
    assert util.password_is_match("password", non_courier_admin.hashed_password)
    response = client.post(
        "/api/auth/courier-admin",
        data={"username": non_courier_admin.email, "password": "password"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login credentials"


@pytest.mark.parametrize(
    "non_vendor_user",
    [
        pytest.lazy_fixture("courier_admin"),
        pytest.lazy_fixture("admin"),
        pytest.lazy_fixture("courier_staff"),
        pytest.lazy_fixture("user"),
    ],
)
def test_authenticate_non_vendor_user_on_vendor_platform_fail(client, non_vendor_user):
    assert util.password_is_match("password", non_vendor_user.hashed_password)
    response = client.post(
        "/api/auth/vendor",
        data={"username": non_vendor_user.email, "password": "password"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login credentials"


@pytest.mark.parametrize(
    "non_courier_user",
    [
        pytest.lazy_fixture("home_vendor_admin"),
        pytest.lazy_fixture("admin"),
        pytest.lazy_fixture("home_vendor_staff"),
        pytest.lazy_fixture("user"),
    ],
)
def test_authenticate_non_courier_user_on_courier_platform_fail(
    client, non_courier_user
):
    assert util.password_is_match("password", non_courier_user.hashed_password)
    response = client.post(
        "/api/auth/courier",
        data={"username": non_courier_user.email, "password": "password"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login credentials"


def test_authenticate_user(client: TestClient, user: models.User):
    assert util.password_is_match("password", user.hashed_password)
    response = client.post(
        "/api/auth",
        data={"username": user.email, "password": "password"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "Bearer"


def test_authenticate_user_with_wrong_credentials_fail(
    client: TestClient, user: models.User
):
    assert util.password_is_match("password", user.hashed_password)
    response = client.post(
        "/api/auth",
        data={"username": user.email, "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login credentials"


@pytest.mark.parametrize(
    "non_user",
    [
        pytest.lazy_fixture("home_vendor_admin"),
        pytest.lazy_fixture("admin"),
        pytest.lazy_fixture("home_vendor_staff"),
        pytest.lazy_fixture("courier_admin"),
        pytest.lazy_fixture("courier_staff"),
    ],
)
def test_authenticate_non_user_on_user_platform_fail(client, non_user):
    assert util.password_is_match("password", non_user.hashed_password)
    response = client.post(
        "/api/auth",
        data={"username": non_user.email, "password": "password"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid login credentials"
