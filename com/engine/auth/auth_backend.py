import os

from dotenv import load_dotenv
from fastapi import Depends
from starlette.authentication import AuthCredentials, SimpleUser, BaseUser, AuthenticationBackend
from starlette.requests import Request
from starlette.exceptions import HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

# Import your existing components
from config import get_db
from com.models.User import User as SQLUser

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

class AuthenticatedUser(BaseUser):
    """Custom user class to hold our SQLAlchemy User object"""
    def __init__(self, user: SQLUser):
        self.user = user

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.user.email # Or user.id, user.username, etc.

    @property
    def identity(self) -> str:
        return str(self.user.id) # Unique identifier for the user

# Define an AnonymousUser for unauthenticated requests
class AnonymousUser(BaseUser):
    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def display_name(self) -> str:
        return "Anonymous"

    @property
    def identity(self) -> str:
        return "anonymous"


class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: Request):
        if "Authorization" not in conn.headers:
            return # No authentication header

        auth_header = conn.headers["Authorization"]
        if not auth_header.startswith("Bearer "):
            return # Not a Bearer token

        token = auth_header.split(" ")[1]

        db: Session = Depends(get_db) # Get a new DB session for the middleware
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")

            if user_id is None:
                return # No user ID in token

            user = db.query(SQLUser).filter(SQLUser.id == user_id).first()
            if user is None:
                return # User not found in DB

            # If authenticated, return AuthCredentials and a user object
            return AuthCredentials(["authenticated"]), AuthenticatedUser(user)

        except JWTError:
            # Token is invalid (malformed, expired, bad signature)
            return # Not authenticated
        except Exception:
            # Catch any other unexpected errors during authentication
            return # Not authenticated
        finally:
            db.close() # Always close the DB session