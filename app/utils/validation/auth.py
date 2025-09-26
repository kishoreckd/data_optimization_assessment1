from fastapi import Header, HTTPException, status
from app.core.config import settings 


async def verify_api_key(api_key: str = Header(...)):
    """
    Verifies the provided Api key in the request headers.
    """
    if api_key != settings.AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or unauthorized Api key."
        )
    return api_key
