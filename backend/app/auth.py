import os
import uuid

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.session import get_db
from backend.auth import hash_password, verify_password

# I create a router so I can register these endpoints in main.py easily
router = APIRouter(prefix="/auth", tags=["auth"])

# I read JWT settings from environment variables
# because I never want secrets hard-coded in the repo
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGO = "HS256"

# I fail fast if JWT_SECRET is missing
# because auth would silently break without a secret key
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET is not set")


@router.post("/register")
def register(user_data: dict, db: Session = Depends(get_db)):
    # I check if the user already exists
    # because I don't want duplicate emails in the database
    existing_user = db.query(User).filter(User.email == user_data["email"]).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # I hash the password before saving
    # because I never store raw passwords in the database
    hashed_password = hash_password(user_data["password"])

    # I create the user record
    new_user = User(
        id=str(uuid.uuid4()),
        email=user_data["email"],
        password_hash=hashed_password
    )

    # I save the user to the database
    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}


@router.post("/login")
def login(user_data: dict, db: Session = Depends(get_db)):
    # I fetch the user by email
    user = db.query(User).filter(User.email == user_data["email"]).first()

    # I validate the password
    if not user or not verify_password(user_data["password"], user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # I generate a JWT token
    token = jwt.encode({"sub": user.id}, JWT_SECRET, algorithm=JWT_ALGO)

    return {"access_token": token}
