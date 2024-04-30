from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Define the base directory for the SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_URL = "sqlite:///" + os.path.join(BASE_DIR, "DB", "database_table.db")

# Define the PostgreSQL database URL
POSTGRES_URL = "postgresql://user:password@postgresserver/db"

# Get the value of the ENVIRONMENT environment variable
environment = os.getenv("ENVIRONMENT", "development")

# Use SQLite for development and testing environments, PostgreSQL for production
if environment == "production":
    SQLALCHEMY_DATABASE_URL = POSTGRES_URL
else:
    SQLALCHEMY_DATABASE_URL = SQLITE_URL

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
