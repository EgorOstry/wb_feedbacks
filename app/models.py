from sqlalchemy import Column, Integer, DateTime, NVARCHAR
from app.database import Base

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(NVARCHAR(50), primary_key=True)
    text = Column(NVARCHAR(4000))
    productValuation = Column(Integer)
    createdDate = Column(DateTime)
    productId = Column(NVARCHAR(9))
    source = Column(NVARCHAR(20))
