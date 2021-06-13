from fastapi import FastAPI
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
    api.include_router(get_admin_router(), prefix="/admin")
    api.include_router(get_courier_admin_router(), prefix="/courier-admin")
    api.include_router(get_vendor_admin_router(), prefix="/vendor-admin")
    api.include_router(get_courier_router(), prefix="/courier")
    api.include_router(get_vendor_router(), prefix="/vendor")
    api.include_router(get_router())
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
