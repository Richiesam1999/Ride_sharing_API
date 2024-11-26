from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from database import Base
from schemas import RideStatus

class RideStatus(enum.Enum):
    REQUESTED = "requested"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    rides = relationship("Ride", back_populates="user")

class Driver(Base):
    __tablename__ = "drivers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    current_location = Column(String)  # Format: "lat,lon(-90 90,-180 180)"
    available = Column(Boolean, default=True)
    rides = relationship("Ride", back_populates="driver")

class Ride(Base):
    __tablename__ = "rides"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    pickup_location = Column(String)  # "latitude,longitude"
    dropoff_location = Column(String)  # "latitude,longitude"
    status = Column(Enum(RideStatus))
    
    user = relationship("User", back_populates="rides")
    driver = relationship("Driver", back_populates="rides")


