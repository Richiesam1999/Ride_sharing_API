from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://admins:admin@localhost:5432/ride_sharing"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
#db_session = scoped_session(SessionLocal)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

