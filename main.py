from fastapi import FastAPI
from routers import rides, drivers,users
from models import Base
from database import engine
from routers import users
#from websocket.ride_track import router as websocket_router

app = FastAPI(title="Ride Sharing Platform API")


# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(rides.router, prefix="/rides", tags=["rides"])
app.include_router(drivers.router, prefix="/drivers", tags=["drivers"])
#app.include_router(websocket_router)

# Create tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)