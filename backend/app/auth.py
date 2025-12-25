import os
import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.session import get_db
from .auth_utils import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

bearer_scheme = HTTPBearer(auto_error=False)

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALGO = "HS256"
JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))


# -----------------------
# Schemas (Pydantic)
# -----------------------
class AuthIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)  # bcrypt limit: 72 bytes (we enforce it)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -----------------------
# Routes
# -----------------------
@router.post("/register")
def register(user_data: AuthIn, db: Session = Depends(get_db)):
    # user_data.password is now guaranteed to be a short string
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)

    new_user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        password_hash=hashed_password,
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}


@router.post("/login", response_model=TokenOut)
def login(user_data: AuthIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    exp = datetime.utcnow() + timedelta(minutes=JWT_EXPIRES_MINUTES)
    payload = {"sub": str(user.id), "exp": exp}

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return {"id": str(user.id), "email": user.email}
