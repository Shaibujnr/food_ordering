from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from foodie import config


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
