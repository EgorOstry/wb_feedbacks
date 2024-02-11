from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os


load_dotenv(override=True)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

Base = declarative_base()


class ProductsMapping(Base):
    __tablename__ = 'products_mapping'

    id = Column(Integer, primary_key=True)
    marketplace_id = Column(Integer)
    internal_code = Column(Integer)
    external_code = Column(Integer, unique=True)


class Feedback(Base):
    __tablename__ = 'feedbacks'

    id = Column(String, primary_key=True)
    text = Column(String)
    product_valuation = Column(Integer)
    created_date = Column(DateTime)
    answer = Column(String)
    state = Column(String)
    imt_id = Column(Integer)
    nm_id = Column(Integer, ForeignKey('products_mapping.external_code'))
    product_name = Column(String)
    supplier_article = Column(String)
    supplier_name = Column(String)
    brand_name = Column(String)
    size = Column(String)
    video = Column(String)
    was_viewed = Column(Boolean)
    photo_links = Column(String)
    user_name = Column(String)
    matching_size = Column(String)
    is_able_supplier_feedback_valuation = Column(Boolean)
    supplier_feedback_valuation = Column(Integer)
    is_able_supplier_product_valuation = Column(Boolean)
    supplier_product_valuation = Column(Integer)
    is_able_return_product_orders = Column(Boolean)
    return_product_orders_date = Column(DateTime)
    bables = Column(String)

    # Связь с таблицей соответствия артикулов
    product_mapping = relationship('ProductsMapping', backref='feedbacks')


# Создание сессии и движка для подключения к БД
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Создание всех таблиц
# Данная команда закоментирована, т.к. таблицы создает Alembic
# Base.metadata.create_all(engine)
