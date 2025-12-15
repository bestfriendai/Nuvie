import os
import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.session import get_db
from .auth_utils import hash_password, verify_password

# I create a router so I can register these endpoints in main.py easily
router = APIRouter(prefix="/auth", tags=["auth"])

# I define a Bearer-token security scheme
# because I want FastAPI to extract "Authorization: Bearer <token>"
bearer_scheme = HTTPBearer(auto_error=False)

# I read JWT settings from environment variables
# because I never want secrets hard-coded in the repo
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")  # fallback prevents Render import crash
JWT_ALGO = "HS256"

# I keep token expiry configurable
# because clients should re-auth after a while
JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))


@router.post("/register")
def register(user_data: dict, db: Session = Depends(get_db)):
    # I validate required fields
    # because dict input can miss keys
    if "email" not in user_data or "password" not in user_data:
        raise HTTPException(status_code=400, detail="email and password are required")

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
    # I validate required fields
    # because dict input can miss keys
    if "email" not in user_data or "password" not in user_data:
        raise HTTPException(status_code=400, detail="email and password are required")

    # I fetch the user by email
    # because email is the login identifier
    user = db.query(User).filter(User.email == user_data["email"]).first()

    # I validate the password
    # because I must reject invalid credentials
    if not user or not verify_password(user_data["password"], user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # I build token payload with expiry
    # because tokens should not live forever
    exp = datetime.utcnow() + timedelta(minutes=JWT_EXPIRES_MINUTES)
    payload = {"sub": str(user.id), "exp": exp}

    # I generate a JWT token
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

    return {"access_token": token, "token_type": "bearer"}


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    # I require the Authorization header
    # because protected endpoints need a token
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    token = credentials.credentials

    # I decode the token
    # because I need to extract the user id (sub)
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # I load the user from DB
    # because token only stores an id
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # I return a simple dict
    # because your feed.py expects user["id"]
    return {"id": str(user.id), "email": user.email}
