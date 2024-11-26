from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from dependencies import create_access_token, decode_access_token
from sqlalchemy.exc import IntegrityError
from utils import find_nearest_driver
from models import User
from schemas import UserCreate, UserResponse,LoginRequest



router = APIRouter()


@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = models.User(
            name=user.name,
            email=user.email
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    

@router.get("/drivers", response_model=list[schemas.DriverResponse])
def get_all_drivers(db: Session = Depends(get_db)):
    drivers = db.query(models.Driver).all()
    return drivers



@router.get("/nearest")
def get_nearest_driver(location: str, db: Session = Depends(get_db)):
    nearest_driver = find_nearest_driver(db, location)
    if not nearest_driver:
        raise HTTPException(status_code=404, detail="No drivers available")
    
    return {
        "driver_id": nearest_driver.id,
        "name": nearest_driver.name,
        "current_location": nearest_driver.current_location
    }

@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    # Extracting email
    email = body.email

    # Check if the user exists in the database
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email")

    # Generate JWT token
    token = create_access_token({"sub": email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def get_current_user(token: str = Depends(decode_access_token), db: Session = Depends(get_db)):
    email = token.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Fetch user from database
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
