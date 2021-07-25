import pytest
import random
from datetime import datetime
from fastapi import FastAPI
from sqlalchemy import MetaData
from sqlalchemy.orm.session import Session
from fastapi.testclient import TestClient
from foodie.config import DATABASE_URL
from foodie.db import models
from foodie.db.base import Base, get_engine, SessionLocal
from foodie.main import get_app
from foodie import util, enums
from collections import namedtuple


AdminDetails = namedtuple(
    "AdminDetails", ["email", "password", "first_name", "last_name"]
)


@pytest.fixture(autouse=True)
def create_test_database():
    engine = get_engine(DATABASE_URL)
    metadata: MetaData = Base.metadata
    metadata.create_all(engine)
    yield  # Run the tests.
    metadata.drop_all(engine)


@pytest.fixture
def app() -> FastAPI:
    return get_app()


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture
def session() -> Session:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def admin_details():
    return AdminDetails("test@admin.com", "password", "Foodie", "Admin")


@pytest.fixture
def admin(session: Session, admin_details: AdminDetails) -> models.Admin:
    admin = models.Admin(
        email=admin_details.email,
        email_verified_on=datetime.utcnow(),
        hashed_password=util.hash_password(admin_details.password),
        first_name=admin_details.first_name,
        last_name=admin_details.last_name,
    )
    session.add(admin)
    session.commit()
    return admin


@pytest.fixture
def admin_auth_header(session: Session, admin: models.Admin) -> dict:
    access_token = util.create_access_token({"sub": str(admin.id)})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def restaurant_vendor(session: Session) -> models.Vendor:
    vendor = models.Vendor(
        name="Restaurant Vendor",
        type=enums.VendorType.RESTAURANT,
        address="restaurant vendor address",
    )
    session.add(vendor)
    session.commit()
    return vendor


@pytest.fixture
def home_vendor(session: Session) -> models.Vendor:
    vendor = models.Vendor(
        name="Home Vendor",
        type=enums.VendorType.HOME,
        address="home vendor address",
    )
    session.add(vendor)
    session.commit()
    return vendor


@pytest.fixture
def food_stand_vendor(session: Session) -> models.Vendor:
    vendor = models.Vendor(
        name="Food Stand Vendor",
        type=enums.VendorType.FOOD_STAND,
        address="food stand vendor",
    )
    session.add(vendor)
    session.commit()
    return vendor


@pytest.fixture
def vendor(restaurant_vendor, home_vendor, food_stand_vendor):
    return random.choice([restaurant_vendor, home_vendor, food_stand_vendor])


@pytest.fixture
def courier(session: Session) -> models.Courier:
    courier = models.Courier(name="Courier Delivery", address="courier address")
    session.add(courier)
    session.commit()
    return courier


@pytest.fixture
def restaurant_vendor_admin(session: Session, restaurant_vendor: models.Vendor):
    vendor_admin = models.VendorUser(
        vendor_id=restaurant_vendor.id,
        first_name="John",
        last_name="Doe",
        role=enums.VendorUserRole.ADMIN,
        phone_number="08012345678",
        email="restaurant_vendor_admin@test.com",
        hashed_password=util.hash_password("password"),
    )
    session.add(vendor_admin)
    session.commit()
    return vendor_admin


@pytest.fixture
def home_vendor_admin(session: Session, home_vendor: models.Vendor):
    vendor_admin = models.VendorUser(
        vendor_id=home_vendor.id,
        first_name="John",
        last_name="Doe",
        role=enums.VendorUserRole.ADMIN,
        phone_number="08012345678",
        email="home_vendor_admin@test.com",
        hashed_password=util.hash_password("password"),
    )
    session.add(vendor_admin)
    session.commit()
    return vendor_admin


@pytest.fixture
def food_stand_vendor_admin(session: Session, food_stand_vendor: models.Vendor):
    vendor_admin = models.VendorUser(
        vendor_id=food_stand_vendor.id,
        first_name="John",
        last_name="Doe",
        role=enums.VendorUserRole.ADMIN,
        phone_number="08012345678",
        email="food_stand_vendor_admin@test.com",
        password=util.hash_password("password"),
    )
    session.add(vendor_admin)
    session.commit()
    return vendor_admin


@pytest.fixture
def restaurant_vendor_staff(session: Session, restaurant_vendor: models.Vendor):
    vendor_staff = models.VendorUser(
        vendor_id=restaurant_vendor.id,
        first_name="John",
        last_name="Doe",
        role=enums.VendorUserRole.STAFF,
        phone_number="08012345678",
        email="restaurant_vendor_staff@test.com",
        hashed_password=util.hash_password("password"),
    )
    session.add(vendor_staff)
    session.commit()
    return vendor_staff


@pytest.fixture
def home_vendor_staff(session: Session, home_vendor: models.Vendor):
    vendor_staff = models.VendorUser(
        vendor_id=home_vendor.id,
        first_name="John",
        last_name="Doe",
        role=enums.VendorUserRole.STAFF,
        phone_number="08012345678",
        email="home_vendor_staff@test.com",
        hashed_password=util.hash_password("password"),
    )
    session.add(vendor_staff)
    session.commit()
    return vendor_staff


@pytest.fixture
def food_stand_vendor_staff(session: Session, food_stand_vendor: models.Vendor):
    vendor_staff = models.VendorUser(
        vendor_id=food_stand_vendor.id,
        first_name="John",
        last_name="Doe",
        role=enums.VendorUserRole.STAFF,
        phone_number="08012345678",
        email="food_stand_vendor_staff@test.com",
        password=util.hash_password("password"),
    )
    session.add(vendor_staff)
    session.commit()
    return vendor_staff


@pytest.fixture
def courier_admin(session: Session, courier: models.Courier):
    courier_admin = models.CourierUser(
        courier_id=courier.id,
        first_name="John",
        last_name="Doe",
        role=enums.CourierUserRole.ADMIN,
        phone_number="08012345678",
        email="courier_admin@test.com",
        hashed_password=util.hash_password("password"),
    )
    session.add(courier_admin)
    session.commit()
    return courier_admin


@pytest.fixture
def courier_staff(session: Session, courier: models.Courier):
    courier_staff = models.CourierUser(
        courier_id=courier.id,
        first_name="John",
        last_name="Doe",
        role=enums.CourierUserRole.STAFF,
        phone_number="08012345678",
        email="courier_staff@test.com",
        hashed_password=util.hash_password("password"),
    )
    session.add(courier_staff)
    session.commit()
    return courier_staff


@pytest.fixture
def user(session: Session):
    now = datetime.utcnow()
    user = models.User(
        email="user@test.com",
        email_verified_on=now,
        hashed_password=util.hash_password("password"),
        first_name="Shaibu",
        last_name="Shaibu",
        phone_number="08012345678",
        phone_number_verified_on=now,
    )
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def restaurant_vendor_admin_auth_header(restaurant_vendor_admin: models.VendorUser):
    access_token = util.create_access_token({"sub": str(restaurant_vendor_admin.id)})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def home_vendor_admin_auth_header(home_vendor_admin: models.VendorUser):
    access_token = util.create_access_token({"sub": home_vendor_admin.id})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def food_stand_vendor_admin_auth_header(food_stand_vendor_admin: models.VendorUser):
    access_token = util.create_access_token({"sub": food_stand_vendor_admin.id})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def restaurant_vendor_staff_auth_header(restaurant_vendor_staff: models.VendorUser):
    access_token = util.create_access_token({"sub": str(restaurant_vendor_staff.id)})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def home_vendor_staff_auth_header(home_vendor_staff: models.VendorUser):
    access_token = util.create_access_token({"sub": home_vendor_staff.id})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def food_stand_vendor_staff_auth_header(food_stand_vendor_staff: models.VendorUser):
    access_token = util.create_access_token({"sub": food_stand_vendor_staff.id})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def courier_admin_auth_header(courier_admin: models.Courier):
    access_token = util.create_access_token({"sub": str(courier_admin.id)})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def courier_staff_auth_header(courier_staff: models.Courier):
    access_token = util.create_access_token({"sub": str(courier_staff.id)})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def user_auth_header(user: models.User):
    access_token = util.create_access_token({"sub": str(user.id)})
    return {"Authorization": f"Bearer {access_token}"}
