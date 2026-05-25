from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists"
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect email or password"
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is expired"
)

NoJWTException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is invalid"
)

NoUserIdException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User ID not found"
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not enough permissions"
)

TokenNotFound = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Token not found"
)

DeviceNotFoundException = HTTPException(
    status_code=404,
    detail='Device not found'
)

MeasurementsNotFoundException = HTTPException(
    status_code=404,
    detail='No measurements found for this period'
)
