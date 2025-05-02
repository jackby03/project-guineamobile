from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from shared.configuration.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


# JWT Token Handling
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token with given payload data and expiration time.
    Args:
        data (dict): The payload data to encode in the token. Must contain 'sub' field as string.
        expires_delta (Optional[timedelta], optional): Custom expiration time delta.
            If None, defaults to ACCESS_TOKEN_EXPIRE_MINUTES.
    Returns:
        str: The encoded JWT token string.
    Raises:
        ValueError: If 'sub' field is missing in data or not a string.
    Example:
        >>> data = {"sub": "user123", "role": "admin"}
        >>> token = create_access_token(data)
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    to_encode.update({"iat": datetime.utcnow()})
    if "sub" not in to_encode or not isinstance(to_encode["sub"], str):
        raise ValueError("The 'sub' field must be a string.")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodes and validates a JWT access token.
    Args:
        token (str): The JWT token string to decode
    Returns:
        Optional[dict]: The decoded token payload as a dictionary if valid,
                       or None if the token is invalid or expired
    Details:
        - Attempts to decode the JWT token using the configured secret key and algorithm
        - Validates the token expiration time if present
        - Returns None if token is invalid, expired or fails to decode
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "exp" in payload:
            expire = datetime.fromtimestamp(payload["exp"])
            if expire < datetime.utcnow():
                return None
        return payload
    except JWTError:
        return None
