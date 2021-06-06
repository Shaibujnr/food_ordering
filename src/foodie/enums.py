from enum import Enum


class VendorType(str, Enum):
    RESTAURANT = "restaurant"
    HOME = "home"
    FOOD_STAND = "food_stand"


class VendorUserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"


class CourierUserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"