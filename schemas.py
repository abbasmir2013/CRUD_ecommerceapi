from pydantic import BaseModel

# Base schema for shared attributes
class PropertyBase(BaseModel):
    title: str
    address: str
    price: float
    bedrooms: int
    is_available: bool = True

# Schema used when creating a new property record (Request Body)
class PropertyCreate(PropertyBase):
    pass

# Schema used when reading data (Response Body)
class PropertyResponse(PropertyBase):
    id: int

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy models
