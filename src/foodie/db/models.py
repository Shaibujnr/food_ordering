from sqlalchemy import Column, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_utils import ChoiceType
from .base import Base
from .mixins import EntityMixin, TimestampMixin
from foodie import enums


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
    vendor_id = Column(ForeignKey("vendor.id"), nullable=False)
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
    courier_id = Column(ForeignKey("courier.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(
        ChoiceType(enums.CourierUserRole, impl=String()),
        nullable=False,
    )
    hashed_password = Column(String, nullable=False)
