from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# I use Bearer auth because the mobile client will send a token in the header
security = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # I block access if the token is missing
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    # Phase 2: I only require the token to exist.
    # Real JWT verification will be implemented in Phase 3.
    return {"id": "u1"}
