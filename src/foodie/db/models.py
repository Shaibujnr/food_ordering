from sqlalchemy import Column, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy_utils import ChoiceType, ScalarListType, UUIDType
from sqlalchemy_utils.models import Timestamp
from .base import Base
from .mixins import EntityMixin, TimestampMixin
from foodie import enums


food_packages_food_categories_association_table = Table(
    "association",
    Base.metadata,
    Column(
        "food_package_id",
        UUIDType(binary=False),
        ForeignKey("food_packages.id"),
    ),
    Column(
        "category_id",
        UUIDType(binary=False),
        ForeignKey("categories.id"),
    ),
)


class AuthBase(Base, EntityMixin, TimestampMixin):
    __abstract__ = True
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)


class Admin(AuthBase):
    """A platform admin"""

    __tablename__ = "admins"


class User(AuthBase):
    """A user that would like to place order for food on this platform"""

    __tablename__ = "users"
    phone_number = Column(String, nullable=False)


class Vendor(Base, EntityMixin, TimestampMixin):
    """
    A food vendor, could be a restaurant or a food stand
    or even a home food vendor.
    """

    __tablename__ = "vendors"
    name = Column(String, nullable=False)
    type = Column(ChoiceType(enums.VendorType, impl=String()), nullable=False)
    address = Column(String, nullable=False)

    # TODO location


class VendorUser(Base, EntityMixin, TimestampMixin):
    """
    A user under a specific vendor with specific roles
    """

    __tablename__ = "vendor_users"
    vendor_id = Column(ForeignKey("vendors.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(
        ChoiceType(enums.VendorUserRole, impl=String()),
        nullable=False,
    )
    hashed_password = Column(String, nullable=False)


class Courier(Base, EntityMixin, TimestampMixin):
    """
    A courier or delivery business, tasked with the
    responsibility of delivering orders to user
    """

    __tablename__ = "couriers"
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    # TODO location


class CourierUser(Base, EntityMixin, TimestampMixin):
    """
    A user under a specific courier with specific roles
    """

    __tablename__ = "courier_users"
    courier_id = Column(ForeignKey("couriers.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(
        ChoiceType(enums.CourierUserRole, impl=String()),
        nullable=False,
    )
    hashed_password = Column(String, nullable=False)


class FoodCategory(Base, EntityMixin, TimestampMixin):
    __tablename__ = "food_categories"
    name = Column(String, nullable=False)


class FoodPackage(Base, EntityMixin, TimestampMixin):
    __tablename__ = "food_packages"
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    items = Column(ScalarListType(str))
    price = Column(String, nullable=False)
    is_available = Column(Boolean, nullable=False, default=True)
    vendor_id = Column(ForeignKey("vendors.id"), nullable=False)
    categories = relationship(
        FoodCategory,
        secondary=food_packages_food_categories_association_table,
    )


class ContactInformation(Base, EntityMixin, TimestampMixin):
    __tablename__ = "contact_informations"
    vendor_id = Column(ForeignKey("vendors.id"), nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)


class OpenInformation(Base, EntityMixin, TimestampMixin):
    __tablename__ = "open_informations"
    __table_args__ = (UniqueConstraint("vendor_id", "day"),)
    vendor_id = Column(ForeignKey("vendors.id"), nullable=False)
    day = Column(
        ChoiceType(enums.DaysOfTheWeek, impl=String()),
        nullable=False,
    )
    open_from = Column(Timestamp)
    open_to = Column(Timestamp)
