# app/init_db.py
from sqlalchemy.orm import Session
from app import models, database

def init_db():
    # Create tables
    models.Base.metadata.create_all(bind=database.engine)

    # Get DB session
    db = database.SessionLocal()

    try:
        # Check if we already have data
        existing_drivers = db.query(models.Driver).first()
        if existing_drivers:
            return "Database already initialized"

        # Add sample drivers
        sample_drivers = [
            models.Driver(
                name="John Doe",
                current_location="40.7128,-74.0060",  # New York
                available=True
            ),
            models.Driver(
                name="Jane Smith",
                current_location="34.0522,-118.2437",  # Los Angeles
                available=True
            ),
            models.Driver(
                name="Bob Johnson",
                current_location="41.8781,-87.6298",  # Chicago
                available=True
            )
        ]
        db.add_all(sample_drivers)

        # Add sample users
        sample_users = [
            models.User(
                name="Alice Brown",
                email="alice@example.com"
            ),
            models.User(
                name="Charlie Davis",
                email="charlie@example.com"
            )
        ]
        db.add_all(sample_users)

        db.commit()
        return "Database initialized with sample data"

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()