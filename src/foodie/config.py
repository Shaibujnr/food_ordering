import os
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from pathlib import Path

APP_ENV: str = os.getenv("APP_ENV", "dev")


# eg .env.dev, .env.production, .env.test
p: Path = Path(__file__).parents[2] / f"env/.{APP_ENV}.env"
config: Config = Config(p if p.exists() else None)

PROJECT_NAME: str = "Foodie"

IS_DEVELOPMENT: bool = APP_ENV == "dev"

IS_TEST: bool = APP_ENV == "test"

IS_PRODUCTION: bool = APP_ENV == "prod"

ALLOWED_HOSTS: CommaSeparatedStrings = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="localhost"
)

DATABASE_URL: str = config("DATABASE_URL", cast=str)

SECRET_KEY: str = config("SECRET_KEY", cast=str)

ACTIVITY_TOKEN_SECRET_KEY: str = config("ACTIVITY_TOKEN_SECRET_KEY", cast=str)

JWT_ALGORITHM: str = config("JWT_ALGORITHM", cast=str, default="HS256")

ACCESS_TOKEN_EXPIRE: int = config("ACCESS_TOKEN_EXPIRE", cast=int, default=60)

CLIENT_HOST: str = config("CLIENT_HOST", cast=str)  # host for frontend

SALT: str = config("SALT", cast=str)
