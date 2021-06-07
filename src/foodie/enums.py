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


class DaysOfTheWeek(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class OrderEventType(str, Enum):
    ORDER_PLACED = "order_placed"
    VENDOR_ACCEPTED = "vendor_accepted"
    VENDOR_REJECTED = "vendor_rejected"
    COURIER_ACCEPTED = "courier_accepted"
    COURIER_REJECTED = "courier_rejected"
    VENDOR_CANCELED = "courier_canceled"
    COURIER_CANCELED = "courier_canceled"
    ORDER_CANCELED = "user_canceled"
    PREPARED_FOR_PICKUP = "ready_for_pickup"
    ORDER_PICKED_UP = "order_picked_up"
    COURIER_REQUESTED = "courier_requested"
    COURIER_NOT_FOUND = "courier_not_found"
    DELIVERY_STARTED = "delivery_started"
    DELIVERED = "delivered"
    CLOSED = "closed"
