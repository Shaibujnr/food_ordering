from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from foodie import config
from foodie.api.router import (
    get_admin_router,
    get_courier_admin_router,
    get_vendor_admin_router,
    get_courier_router,
    get_vendor_router,
    get_router,
)
from foodie.api.deps import (
    get_current_admin,
    get_current_courier_admin,
    get_current_vendor_admin,
    get_current_courier,
    get_current_vendor,
)


def get_api_app():
    """
    Returns and configures a FastAPI application
    for api endpoints
    """

    api = FastAPI(title=config.PROJECT_NAME, root_path="/api")

    api.add_middleware(
        CORSMiddleware,
        allow_origins=list(config.ALLOWED_HOSTS),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    api.include_router(
        get_admin_router(),
        dependencies=[Depends(get_current_admin)],
        prefix="/admin",
        tags=["Admin Routes"],
    )
    api.include_router(
        get_courier_admin_router(),
        dependencies=[Depends(get_current_courier_admin)],
        prefix="/courier-admin",
        tags=["Courier Admin Routes"],
    )
    api.include_router(
        get_vendor_admin_router(),
        dependencies=[Depends(get_current_vendor_admin)],
        prefix="/vendor-admin",
        tags=["Vendor Admin Routes"],
    )
    api.include_router(
        get_vendor_router(),
        dependencies=[Depends(get_current_vendor)],
        prefix="/vendor",
        tags=["Vendor Routes"],
    )
    api.include_router(
        get_courier_router(),
        dependencies=[Depends(get_current_courier)],
        prefix="/courier",
        tags=["Courier Routes"],
    )

    api.include_router(get_router(), tags=["User Routes"])
    return api


def get_app() -> FastAPI:
    """
    Construct main fastapi application and
    mount api application on path /api
    """
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    api_app = get_api_app()
    app.mount("/api", app=api_app)
    return app


app: FastAPI = get_app()
