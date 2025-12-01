# auth/dependencies.py
from tracemalloc import start
from fastapi import Header, HTTPException
from .google_verify import verify_google_token
import time

async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization")

    start = time.time()
# ... code
    print("get_current_user took", time.time() - start, "seconds") 
    token = authorization.replace("Bearer ", "")
    user_id = verify_google_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_id
