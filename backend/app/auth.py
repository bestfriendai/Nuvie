import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext

security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGO = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# I hash the password to store it safely in the database
def hash_password(password: str):
    return pwd_context.hash(password)

# I verify the password during login
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
