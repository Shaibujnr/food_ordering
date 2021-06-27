from fastapi import status, HTTPException

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_login_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid login credential",
    headers={"WWW-Authenticate": "Bearer"},
)

vendor_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found"
)

courier_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Courier not found"
)

vendor_user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Vendor user not found"
)

courier_user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Courier user not found"
)

invalid_or_expired_token_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
)
