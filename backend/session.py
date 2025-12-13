import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# I read DATABASE_URL from env so secrets never live in the codebase
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    # I create one DB session per request and close it safely
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
