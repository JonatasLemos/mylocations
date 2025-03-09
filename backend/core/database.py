import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Function to handle database connection
    to be used as a dependency in FastAPI endpoints

    Yields:
        _type_: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
