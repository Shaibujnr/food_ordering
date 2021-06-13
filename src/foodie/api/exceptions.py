from fastapi import status, HTTPException


invalid_login_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid login credential",
    headers={"WWW-Authenticate": "Bearer"},
)
