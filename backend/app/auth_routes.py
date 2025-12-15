from fastapi import APIRouter, HTTPException, Depends
from jose import jwt
import uuid
import os

from backend.models.user import User
from backend.session import get_db
from backend.auth import hash_password, verify_password

# I create an API router for authentication-related endpoints
# because I want to group login and register logic under /auth
router = APIRouter(prefix="/auth", tags=["auth"])

# I read the JWT secret from environment variables
# because secrets should never be hard-coded
JWT_SECRET = os.getenv("JWT_SECRET")

# I define the JWT algorithm explicitly
# because both encoding and decoding must use the same algorithm
JWT_ALGO = "HS256"


@router.post("/register")
def register(user_data: dict, db=Depends(get_db)):
    # I check if a user with the same email already exists
    # because I want to prevent duplicate accounts
    existing_user = db.query(User).filter(User.email == user_data["email"]).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # I hash the user's password before saving it
    # because storing plain text passwords is a security risk
    hashed_password = hash_password(user_data["password"])

    # I create a new user with a UUID as the primary key
    # because UUIDs are safer than incremental IDs in distributed systems
    new_user = User(
        id=str(uuid.uuid4()),
        email=user_data["email"],
        password_hash=hashed_password
    )

    # I add the new user to the database session
    db.add(new_user)

    # I commit the transaction to persist the user
    db.commit()

    # I return a simple success message
    # because the client only needs to know the operation succeeded
    return {"message": "User registered successfully"}


@router.post("/login")
def login(user_data: dict, db=Depends(get_db)):
    # I fetch the user by email from the database
    # because email is the unique login identifier
    user = db.query(User).filter(User.email == user_data["email"]).first()

    # I verify both user existence and password correctness
    # because I must reject invalid credentials
    if not user or not verify_password(user_data["password"], user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # I generate a JWT token with the user ID as the subject
    # because the token will identify the user in future requests
    token = jwt.encode(
        {"sub": user.id},
        JWT_SECRET,
        algorithm=JWT_ALGO
    )

    # I return the access token to the client
    # because the client will attach it to Authorization headers
    return {"access_token": token}
