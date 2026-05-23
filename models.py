from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    address = Column(String)
    price = Column(Float)
    bedrooms = Column(Integer)
    is_available = Column(Boolean, default=True)
