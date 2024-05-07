from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app import config


engine = create_engine(
    config.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()