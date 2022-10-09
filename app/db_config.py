import logging
import os
import platform

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

from app.app_config import get_module_logger

logger: logging.Logger = get_module_logger("db_config")

dotenv_path = os.path.join(os.getcwd(), "../.env")
load_dotenv(dotenv_path)

db_host = "localhost" if platform.system() == "Windows" else {os.getenv('DB_HOST')}

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:" \
                          f"{os.getenv('DB_PASSWORD')}@{db_host}:5432/{os.getenv('DB_NAME')}"

is_file = os.path.isfile(dotenv_path)
if not is_file:
    SQLALCHEMY_DATABASE_URL = 'sqlite:///restaurant_rating.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

sessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
session = Session(engine)
Session = sessionmaker()

logger.info('DB loaded')
