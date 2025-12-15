from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import uuid
import os

from backend.models.user import User
from backend.session import get_db
from backend.auth import hash_password, verify_password

# I create an API router for authentication-related endpoints
# because I want to group login and register logic under /auth
router = APIRouter(prefix="/auth", tags=["auth"])

# I define a reusable HTTP Bearer scheme
# because JWT tokens are sent via Authorization: Bearer <token>
security = HTTPBearer()

# I read the JWT secret from environment variables
# because secrets should never be hard-coded
JWT_SECRET = os.getenv("JWT_SECRET")

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET is not set")

# I define the JWT algorithm explicitly
JWT_ALGO = "HS256"


@router.post("/register")
def register(user_data: dict, db=Depends(get_db)):
    # I check if a user with the same email already exists
    existing_user = db.query(User).filter(User.email == user_data["email"]).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # I hash the user's password before saving it
    hashed_password = hash_password(user_data["password"])

    # I create a new user with a UUID
    new_user = User(
        id=str(uuid.uuid4()),
        email=user_data["email"],
        password_hash=hashed_password,
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}


@router.post("/login")
def login(user_data: dict, db=Depends(get_db)):
    # I fetch the user by email
    user = db.query(User).filter(User.email == user_data["email"]).first()

    # I validate credentials
    if not user or not verify_password(user_data["password"], user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # I generate a JWT token
    token = jwt.encode(
        {"sub": user.id},
        JWT_SECRET,
        algorithm=JWT_ALGO,
    )

    return {"access_token": token}


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db),
):
    # I extract the raw token
    token = credentials.credentials

    try:
        # I decode the JWT
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    # I fetch the user from the database
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # I return a minimal user context
    return {
        "id": user.id,
        "email": user.email,
    }
