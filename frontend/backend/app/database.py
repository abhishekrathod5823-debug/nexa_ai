# database.py
# Yeh file MySQL se connection banati hai SQLAlchemy ka use karke

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# Database connection URL banate hain
# Format: mysql+pymysql://username:password@host:port/database_name
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Engine banate hain - yeh asli connection handle karta hai
engine = create_engine(DATABASE_URL)

# SessionLocal - har request ke liye ek naya database session banayega
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base - hamare saare models (tables) isi se inherit karenge
Base = declarative_base()


# Dependency function - FastAPI isko use karega database session dene ke liye
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()