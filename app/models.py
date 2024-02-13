from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class ProductsMapping(Base):
    __tablename__ = 'products_mapping'
    id = Column(Integer, primary_key=True)
    marketplace_id = Column(Integer)
    internal_code = Column(String)
    external_code = Column(String, unique=True)
    product_details = relationship("ProductDetails", back_populates="product_mapping")


class ProductDetails(Base):
    __tablename__ = 'product_details'
    id = Column(Integer, primary_key=True)
    imtId = Column(Integer, name='imt_id')
    nmId = Column(Integer, ForeignKey('products_mapping.id'))
    productName = Column(String, name='product_name')
    supplierArticle = Column(String, name='supplier_article')
    supplierName = Column(String, name='supplier_name')
    brandName = Column(String, name='brand_name')
    size = Column(String)
    feedbacks = relationship("Feedback", back_populates="productDetail")


class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(String, primary_key=True)
    text = Column(String)
    productValuation = Column(Integer, name='product_valuation')
    createdDate = Column(DateTime, name='created_date')
    answer = Column(String)
    state = Column(String)
    video = Column(String)
    wasViewed = Column(Boolean, name='was_viewed')
    photoLinks = Column(String, name='photo_links')
    userName = Column(String, name='user_name')
    matchingSize = Column(String, name='matching_size')
    isAbleSupplierFeedbackValuation = Column(Boolean, name='is_able_supplier_feedback_valuation')
    supplierFeedbackValuation = Column(Integer, name='supplier_feedback_valuation')
    isAbleSupplierProductValuation = Column(Boolean, name='is_able_supplier_product_valuation')
    supplierProductValuation = Column(Integer, name='supplier_product_valuation')
    isAbleReturnProductOrders = Column(Boolean, name='is_able_return_product_orders')
    returnProductOrdersDate = Column(DateTime, name='return_product_orders_date')
    bables = Column(String)
    productDetailId = Column(Integer, ForeignKey('product_details.id'), name='product_detail_id')
    productDetail = relationship("ProductDetails", back_populates="feedbacks")
