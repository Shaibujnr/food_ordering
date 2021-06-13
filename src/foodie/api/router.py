from fastapi import APIRouter
from foodie.api.auth import (
    auth_router,
    admin_auth_router,
    vendor_admin_auth_router,
    courier_admin_auth_router,
    vendor_auth_router,
    courier_auth_router,
)


def get_admin_router():
    """Router for all admin endpoints"""
    admin_router = APIRouter()
    admin_router.include_router(admin_auth_router, tags=["Authentication"])
    return admin_router


def get_vendor_admin_router():
    """Router for all vendor admin endpoints"""
    vendor_admin_router = APIRouter()
    vendor_admin_router.include_router(
        vendor_admin_auth_router, tags=["Authentication"]
    )
    return vendor_admin_router


def get_courier_admin_router():
    """Router for all courier admin endpoints"""
    courier_admin_router = APIRouter()
    courier_admin_router.include_router(
        courier_admin_auth_router, tags=["Authentication"]
    )
    return courier_admin_router


def get_vendor_router():
    """Router for all vendor endpoints"""
    vendor_router = APIRouter()
    vendor_router.include_router(vendor_auth_router, tags=["Authentication"])
    return vendor_router


def get_courier_router():
    """Router for all courier endpoints"""
    courier_router = APIRouter()
    courier_router.include_router(courier_auth_router, tags=["Authentication"])
    return courier_router


def get_router():
    """Router for all other endpoints"""
    router = APIRouter()
    router.include_router(auth_router, tags=["Authentication"])
    return router
