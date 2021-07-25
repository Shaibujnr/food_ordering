from sqlalchemy import (
    Column,
    String,
    Table,
    UniqueConstraint,
    Time,
    Boolean,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_utils import ChoiceType, ScalarListType, UUIDType, JSONType
from .base import Base
from .mixins import EntityMixin, TimestampMixin
from foodie import enums


food_packages_food_categories_association_table = Table(
    "food_packages_food_categories_association",
    Base.metadata,
    Column(
        "food_package_id",
        UUIDType(binary=False),
        ForeignKey("food_packages.id"),
    ),
    Column(
        "category_id",
        UUIDType(binary=False),
        ForeignKey("food_categories.id"),
    ),
)


class AuthBase(Base, EntityMixin, TimestampMixin):
    __abstract__ = True
    email = Column(String, nullable=False, unique=True)
    email_verified_on = Column(DateTime, nullable=True)
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
    phone_number_verified_on = Column(DateTime, nullable=False)


class Vendor(Base, EntityMixin, TimestampMixin):
    """
    A food vendor, could be a restaurant or a food stand
    or even a home food vendor.
    """

    __tablename__ = "vendors"
    name = Column(String, nullable=False, unique=True)
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

    vendor = relationship(Vendor, backref="users")


class Courier(Base, EntityMixin, TimestampMixin):
    """
    A courier or delivery business, tasked with the
    responsibility of delivering orders to user
    """

    __tablename__ = "couriers"
    name = Column(String, nullable=False, unique=True)
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

    courier = relationship(Courier, backref="users")


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
    open_from = Column(Time)
    open_to = Column(Time)


class Order(Base, EntityMixin, TimestampMixin):
    __tablename__ = "orders"
    user_id = Column(ForeignKey("users.id"), nullable=False)
    vendor_id = Column(ForeignKey("vendors.id"), nullable=False)
    courier_user_id = Column(ForeignKey("courier_users.id"), nullable=True)
    vendor_accepted = Column(Boolean, nullable=True)
    courier_accepted = Column(Boolean, nullable=True)


class OrderEvent(Base, EntityMixin, TimestampMixin):
    __tablename__ = "order_events"
    order_id = Column(ForeignKey("orders.id"), nullable=False)
    event_type = Column(
        ChoiceType(enums.OrderEventType, impl=String()),
        nullable=False,
    )
    payload = Column(JSONType, nullable=False)


class UserVendorFeedback(Base, EntityMixin, TimestampMixin):
    __tablename__ = "user_vendor_feedbacks"
    __table_args__ = (UniqueConstraint("vendor_id", "user_id"),)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    vendor_id = Column(ForeignKey("vendors.id"), nullable=False)
    rating = Column(Float, nullable=False)
    feedback = Column(String, nullable=True)


class UserFoodPackageFeedback(Base, EntityMixin, TimestampMixin):
    __tablename__ = "user_food_package_feedbacks"
    __table_args__ = (UniqueConstraint("food_package_id", "user_id"),)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    food_package_id = Column(ForeignKey("food_packages.id"), nullable=False)
    rating = Column(Float, nullable=False)
    feedback = Column(String, nullable=True)


class UserCourierFeedback(Base, EntityMixin, TimestampMixin):
    __tablename__ = "user_courier_feedbacks"
    __table_args__ = (UniqueConstraint("courier_id", "user_id"),)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    courier_id = Column(ForeignKey("couriers.id"), nullable=False)
    rating = Column(Float, nullable=False)
    feedback = Column(String, nullable=True)
