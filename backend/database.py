from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from env import *
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect

DATABASE_URL = f"postgresql+pg8000://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
logger.debug(f"DB URL = [{DATABASE_URL}]")

# Création de l'engine et de la session

def get_db_engine():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            logger.info("Database connection successful!")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise e
    return engine

def get_session_maker():
    if get_session_maker.SessionLocal is not None:
        return get_session_maker.SessionLocal
    get_session_maker.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_db_engine())
    return get_session_maker.SessionLocal
get_session_maker.SessionLocal = None

Base = declarative_base()
from models import *

def get_db():
    db = get_session_maker()()
    try:
        yield db
    finally:
        db.close()