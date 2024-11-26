from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from routers.users import get_current_user
from schemas import RideStatus

router = APIRouter()


@router.post("/", response_model=schemas.DriverResponse)
def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    new_driver = models.Driver(
        name=driver.name,
        available=driver.available,
        current_location=driver.current_location
    )
    
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver


@router.put("/{driver_id}/availability")
def update_driver_availability(
    driver_id: int,
    availability: schemas.DriverAvailability,
    db: Session = Depends(get_db)
):
    driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    driver.available = availability.available
    driver.current_location = availability.current_location
    db.commit()
    db.refresh(driver)
    return {"status": "success"}





    
# @router.get("/nearest")
# def get_nearest_driver(location: str, db: Session = Depends(get_db)):
#     try:
#         lat, lon = location.split(",")
#         available_drivers = db.query(models.Driver).filter(models.Driver.available == True).all()
        
#         if not available_drivers:
#             raise HTTPException(status_code=404, detail="No available drivers found")
            
#         nearest_driver = min(
#             available_drivers,
#             key=lambda driver: calculate_distance(
#                 lat, lon,
#                 *driver.current_location.split(",")
#             )
#         )
        
#         return {
#             "driver_id": nearest_driver.id,
#             "name": nearest_driver.name,
#             "current_location": nearest_driver.current_location
#         }
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))