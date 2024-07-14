from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

load_dotenv(override=True)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER")

Base = declarative_base()

# Создание сессии и движка для подключения к БД
DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?driver={DB_DRIVER}&charset=utf8"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Создание всех таблиц
Base.metadata.create_all(engine)
