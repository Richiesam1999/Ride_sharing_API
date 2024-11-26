from pydantic import BaseModel, field_validator
from typing import Optional
from enum import Enum

class RideStatus(str, Enum):
    REQUESTED = "requested"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class RideRequest(BaseModel):
    user_id: int
    pickup_location: str
    dropoff_location: str

    @field_validator('pickup_location', 'dropoff_location')
    def validate_location(cls, v):
        try:
            lat, lon = map(float, v.split(","))
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValueError("Invalid coordinates range")
            return v
        except:
            raise ValueError("Location must be in format 'latitude,longitude'")

class RideResponse(BaseModel):
    id: int
    user_id: int
    driver_id: Optional[int]
    pickup_location: str
    dropoff_location: str
    status: RideStatus

    class Config:
        orm_mode = True

class DriverAvailability(BaseModel):
    available: bool
    current_location: str

    @field_validator('current_location')
    def validate_location(cls, v):
        try:
            lat, lon = map(float, v.split(","))
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValueError("Invalid coordinates range")
            return v
        except:
            raise ValueError("Location must be in format 'latitude,longitude'")
        
class DriverCreate(BaseModel):
    name: str
    available: bool = True  # default to True
    current_location: str

    @field_validator('current_location')
    def validate_location(cls, v):
        try:
            lat, lon = map(float, v.split(","))
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValueError("Invalid coordinates range")
            return v
        except:
            raise ValueError("Location must be in format 'latitude,longitude'")

class DriverResponse(BaseModel):
    id: int
    name: str
    available: bool
    current_location: str

    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    name: str
    email: str

    @field_validator('email')
    def validate_email(cls, v):
        if not '@' in v:
            raise ValueError('Invalid email address')
        return v

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: str