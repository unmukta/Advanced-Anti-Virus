# dlp/core/auth/simple_auth.py
from fastapi import HTTPException, Header

async def verify_token(authorization: str = Header(None)):
    \"\"\"Simple token verification - will be enhanced later\"\"\"
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    return True
