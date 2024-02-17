from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductDetails(Base):
    __tablename__ = 'product_details'
    id = Column(Integer, primary_key=True)
    imtId = Column(Integer)
    nmId = Column(Integer)
    productName = Column(String)
    supplierArticle = Column(String)
    supplierName = Column(String)
    brandName = Column(String)
    size = Column(String)
    feedbacks = relationship("Feedback", back_populates="productDetail")


class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(String, primary_key=True)
    text = Column(String)
    productValuation = Column(Integer)
    createdDate = Column(DateTime)
    # answer = Column(String)
    state = Column(String)
    # video = Column(String)
    wasViewed = Column(Boolean)
    # photoLinks = Column(String)
    userName = Column(String)
    matchingSize = Column(String)
    isAbleSupplierFeedbackValuation = Column(Boolean)
    supplierFeedbackValuation = Column(Integer)
    isAbleSupplierProductValuation = Column(Boolean)
    supplierProductValuation = Column(Integer)
    isAbleReturnProductOrders = Column(Boolean)
    returnProductOrdersDate = Column(DateTime)
    bables = Column(String)
    productDetailId = Column(Integer, ForeignKey('product_details.id'))
    productDetail = relationship("ProductDetails", back_populates="feedbacks")
