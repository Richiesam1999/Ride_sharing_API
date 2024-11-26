from math import radians, sin, cos, sqrt, atan2
import models

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c

def find_nearest_driver(db, location):
    lat1, lon1 = map(float, location.split(","))     #floating pt numbers
    available_drivers = db.query(models.Driver).filter(models.Driver.available == True).all()
    
    if not available_drivers:
        return None

    def calculate_distance_to_driver(driver):
        lat2, lon2 = map(float, driver.current_location.split(","))    
        return calculate_distance(lat1, lon1, lat2, lon2)
    
    return min(available_drivers, key=calculate_distance_to_driver)
