# app/auth/jwt_security.py

import logging
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session # No need for make_transient here anymore
from config import get_db
from com.models.User import User as SQLUser # Your SQLAlchemy User model
from com.schemas.user import TokenData
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 52560000)) # Default to ~100 years if not set

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Configure logging for better insights
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    """
    Creates a JWT access token with a configurable expiration.
    The 'roles' key is expected in the data dictionary.
    """
    to_encode = data.copy()

    # Calculate expiration based on ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # The 'exp' claim is crucial for JWT expiration

    # Log token creation details
    logger.info(f"Creating access token for sub: {to_encode.get('sub')} with expiration: {expire}")

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Decodes a JWT access token.
    Raises HTTPException if decoding fails (e.g., invalid token, expired token).
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token has expired.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        logger.warning("Invalid JWT token.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Unexpected error decoding JWT: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="An unexpected error occurred during token validation",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependency to get the current authenticated human user.
    Retrieves user from DB and ensures they are active.
    Populates user.roles_from_token with roles from the JWT.
    """
    payload = decode_access_token(token)

    username: str = payload.get("sub")
    # Get roles as a list of strings from the token
    roles_from_token: list[str] = payload.get("roles", [])

    if username is None:
        logger.warning("Token payload missing 'sub' (username).")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: Missing username in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Use TokenData for consistency and clarity of what's in the token
    token_data = TokenData(username=username, roles=roles_from_token)

    # Fetch the User object from the DB.
    # No eager loading of `roles` is needed here because we are not using the ORM-managed `user.roles`
    # relationship for token-based roles.
    user = db.query(SQLUser).filter(SQLUser.username == token_data.username).first()
    if user is None:
        logger.warning(f"User '{username}' not found in DB.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # --- CRITICAL CHANGE FOR SOLUTION 2 ---
    # Assign the list of strings from the token to the new `roles_from_token` attribute.
    # This attribute is NOT managed by SQLAlchemy's ORM and can directly accept a list.
    user.roles_from_token = roles_from_token
    logger.debug(f"Assigned roles from token to user object: {user.roles_from_token}")

    return user

def role_required(required_roles: list[str]):
    """
    Higher-order dependency to check if the current user has the required roles.
    Assumes `get_current_user` has already populated roles in the user object's `roles_from_token` attribute.
    """
    def role_checker(current_user: SQLUser = Depends(get_current_user)):
        # --- CRITICAL CHANGE FOR SOLUTION 2 ---
        # Check the new 'roles_from_token' attribute
        if not hasattr(current_user, 'roles_from_token') or not isinstance(current_user.roles_from_token, list):
            logger.error(f"User object for '{current_user.username}' is missing or has invalid 'roles_from_token' attribute. This indicates a setup error.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server configuration error: User roles from token not properly defined.",
            )

        # Check if the user has at least one of the required roles
        if not any(role in current_user.roles_from_token for role in required_roles):
            logger.warning(f"User '{current_user.username}' attempted to access role-restricted endpoint without required roles: {required_roles}. User roles from token: {current_user.roles_from_token}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user # Return the authenticated and authorized user
    return role_checker # Return the inner dependency function