from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from routers.users import get_current_user
#from math import radians, sin, cos, sqrt, atan2
from utils import find_nearest_driver

router = APIRouter()



@router.post("/request", response_model=schemas.RideResponse)
def request_ride(
    ride_request: schemas.RideRequest, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Using the authenticated user's ID 
    user_id = current_user.id
    
    # Optional user exists check 
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Find the nearest driver
    nearest_driver = find_nearest_driver(db, ride_request.pickup_location)
    if not nearest_driver:
        raise HTTPException(status_code=404, detail="No drivers available")

    # Create the ride and assign the driver
    ride = models.Ride(
        user_id=user_id,
        driver_id=nearest_driver.id,
        pickup_location=ride_request.pickup_location,
        dropoff_location=ride_request.dropoff_location,
        status=models.RideStatus.REQUESTED
    )
    
    # logic driver unavailable - since he's committed
    nearest_driver.available = False
    
    db.add(ride)
    db.commit()
    db.refresh(ride)
    
    return ride



@router.get("/{ride_id}", response_model=schemas.RideResponse)
def get_ride_details(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # Authenticate and fetch current user
):
    # Fetching the ride from the database
    ride = db.query(models.Ride).filter(models.Ride.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    if ride.user_id != current_user.id :
        raise HTTPException(status_code=403, detail="Not authorized to view this ride")
    
    return ride







# @router.post("/request", response_model=schemas.RideResponse)
# def request_ride(ride_request: schemas.RideRequest, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
#     # Check if user exists
#     # Use the authenticated user's ID instead of passing it in the body
#     user_id = current_user.id
#     user = db.query(models.User).filter(models.User.id == ride_request.user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # Find the nearest driver
#     nearest_driver = find_nearest_driver(db, ride_request.pickup_location)
#     if not nearest_driver:
#         raise HTTPException(status_code=404, detail="No drivers available within 200 meters")

#     # Create the ride and assign the driver
#     ride = models.Ride(
#         user_id=ride_request.user_id,
#         driver_id=nearest_driver.id,
#         pickup_location=ride_request.pickup_location,
#         dropoff_location=ride_request.dropoff_location,
#         status=models.RideStatus.REQUESTED
#     )
    
#     # Mark driver as unavailable
#     nearest_driver.available = False
    
#     db.add(ride)
#     db.commit()
#     db.refresh(ride)
    
#     return ride





# @router.get("/{ride_id}", response_model=schemas.RideResponse)
# def get_ride_details(ride_id: int, db: Session = Depends(get_db)):
#     ride = db.query(models.Ride).filter(models.Ride.id == ride_id).first()
#     if ride is None:
#         raise HTTPException(status_code=404, detail="Ride not found")
#     return ride






# @router.post("/start_ride/{ride_id}")
# async def start_ride(ride_id: int):
#     # Update ride status in database
#     ride = db_session.query(Ride).filter(Ride.id == ride_id).first()
#     if not ride:
#         raise HTTPException(status_code=404, detail="Ride not found")
#     ride.status = "started"
#     db_session.commit()

#     # Notify connected clients
#     await manager.broadcast(f"Ride {ride_id} status updated to 'started'")
#     return {"message": f"Ride {ride_id} has started."}


# @router.post("/complete_ride/{ride_id}")
# async def complete_ride(ride_id: int):
#     # Update ride status in database
#     ride = db_session.query(Ride).filter(Ride.id == ride_id).first()
#     if not ride:
#         raise HTTPException(status_code=404, detail="Ride not found")
#     ride.status = "completed"
#     db_session.commit()

#     # Notify connected clients
#     await manager.broadcast(f"Ride {ride_id} status updated to 'completed'")
#     return {"message": f"Ride {ride_id} has been completed."}