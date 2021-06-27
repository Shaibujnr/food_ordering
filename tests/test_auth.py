from tests.conftest import AdminDetails
from sqlalchemy.orm.session import Session
from starlette.testclient import TestClient

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
