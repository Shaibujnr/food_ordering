from sqlalchemy import (
    Column,
    String,
    Table,
    UniqueConstraint,
    Time,
    Boolean,
    DateTime,
    Float,
    Numeric,
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


class Org(Base, EntityMixin, TimestampMixin):
    __tablename__ = "orgs"
    org_type = Column(ChoiceType(enums.OrgType, impl=String()), nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    # TODO location column (lat, lng)

    __table_args__ = (UniqueConstraint("org_type", "name"),)
    __mapper_args__ = {"polymorphic_on": org_type}


class Vendor(Org):
    __tablename__ = "vendors"
    id = Column(ForeignKey("orgs.id"), primary_key=True)
    vendor_type = Column(ChoiceType(enums.VendorType, impl=String()), nullable=False)

    __mapper_args__ = {"polymorphic_identity": enums.OrgType.VENDOR}


class Courier(Org):
    __tablename__ = "couriers"
    id = Column(ForeignKey("orgs.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": enums.OrgType.COURIER}


class Admin(Base, EntityMixin, TimestampMixin):
    """A platform admin"""

    __tablename__ = "admins"
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)


class User(Base, EntityMixin, TimestampMixin):
    """A user that would like to place order for food on this platform"""

    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    email_verified_on = Column(DateTime, nullable=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    phone_number_verified_on = Column(DateTime, nullable=False)


class OrgUser(Base, EntityMixin, TimestampMixin):
    __tablename__ = "org_users"
    user_id = Column(ForeignKey("users.id"), nullable=False, unique=True)
    org_id = Column(ForeignKey("orgs.id"), nullable=False)
    role = Column(ChoiceType(enums.OrgUserRole, impl=String()), nullable=False)


class FoodCategory(Base, EntityMixin, TimestampMixin):
    __tablename__ = "food_categories"
    name = Column(String, nullable=False)


class FoodPackage(Base, EntityMixin, TimestampMixin):
    __tablename__ = "food_packages"
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    items = Column(ScalarListType(str))
    price = Column(Numeric, nullable=False)
    is_available = Column(Boolean, nullable=False, default=True)
    vendor_id = Column(ForeignKey("vendors.id"), nullable=False)
    categories = relationship(
        FoodCategory,
        secondary=food_packages_food_categories_association_table,
    )


class ContactInformation(Base, EntityMixin, TimestampMixin):
    __tablename__ = "contact_informations"
    org_id = Column(ForeignKey("orgs.id"), nullable=False)
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
    courier_user_id = Column(ForeignKey("org_users.id"), nullable=True)
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
    __table_args__ = (UniqueConstraint("courier_user_id", "user_id"),)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    courier_user_id = Column(ForeignKey("org_users.id"), nullable=False)
    rating = Column(Float, nullable=False)
    feedback = Column(String, nullable=True)
