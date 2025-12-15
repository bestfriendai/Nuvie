# I define a basic User model to store auth information
from sqlalchemy import Column, String
from backend.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
