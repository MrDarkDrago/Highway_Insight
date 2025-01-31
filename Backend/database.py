from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (you can change the database name as needed)
DATABASE_URL = "mysql+pymysql://root:1234@localhost/highway_insight"

engine = create_engine(DATABASE_URL, echo=True)  # Set echo=True for debugging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create tables (if they don't exist)
Base.metadata.create_all(bind=engine)
