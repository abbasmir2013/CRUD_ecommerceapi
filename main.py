from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
from database import engine, get_db
from schemas import PropertyCreate, PropertyResponse

# Create the database tables automatically on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real Estate Property CRUD API")


# --- CREATE ---
@app.post("/properties/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
def create_property(property_data: PropertyCreate, db: Session = Depends(get_db)):
    db_property = models.Property(**property_data.model_dump())
    db.add(db_property)
    db.commit()
    db.refresh(db_property) # Get the generated ID back from the DB
    return db_property


# --- READ ALL (With filtering) ---
@app.get("/properties/", response_model=List[PropertyResponse])
def read_properties(max_price: float = None, db: Session = Depends(get_db)):
    query = db.query(models.Property)
    if max_price:
        query = query.filter(models.Property.price <= max_price)
    return query.all()


# --- READ ONE ---
@app.get("/properties/{property_id}", response_model=PropertyResponse)
def read_property(property_id: int, db: Session = Depends(get_db)):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property


# --- UPDATE ---
@app.put("/properties/{property_id}", response_model=PropertyResponse)
def update_property(property_id: int, updated_data: PropertyCreate, db: Session = Depends(get_db)):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # Dynamically update values
    for key, value in updated_data.model_dump().items():
        setattr(db_property, key, value)
        
    db.commit()
    db.refresh(db_property)
    return db_property


# --- DELETE ---
@app.delete("/properties/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(property_id: int, db: Session = Depends(get_db)):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    db.delete(db_property)
    db.commit()
    return None
