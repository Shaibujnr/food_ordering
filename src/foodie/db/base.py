from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from foodie.config import DATABASE_URL


def get_engine(database_url):
    if "sqlite" in database_url:
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
        )
    else:
        engine = create_engine(database_url, pool_size=20, max_overflow=10)
    return engine


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=get_engine(DATABASE_URL)
)

Base = declarative_base()
