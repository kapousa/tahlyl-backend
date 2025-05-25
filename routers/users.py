import uuid
from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import get_db
from com.engine.security import create_access_token, verify_password, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES, \
    get_current_user
from com.models.User import User as SQLUser
from com.schemas.user import User, UserCreate, Token

router = APIRouter(prefix="/users", tags=["users"])

# --- Temporary Flag to Disable Authentication ---
DISABLE_AUTH = False

# --- Fake User and Token Generation for Temporary Bypass ---
class FakeUser:
    def __init__(self, id="test_user", name="kapo", email="hatemn2001@yahoo.com"):
        self.id = id
        self.name = name
        self.email = email

def fake_create_access_token(data: dict, expires_delta: timedelta = None):
    """Temporary function to create a fake access token."""
    return "fake_access_token_for_" + data.get("sub", "test_user")

async def get_fake_current_user():
    """Temporary function to bypass authentication and return a fake user."""
    return FakeUser()

@router.get(("/"))
def user_index():
    return {"message": "Welcome user"}

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = SQLUser(id=str(uuid.uuid4()), username=user.username, email=user.email, password=hashed_password, avatar="", role="patient")
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="name or email already registered")

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if DISABLE_AUTH:
        fake_user = FakeUser(name=form_data.username)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = fake_create_access_token(data={"sub": fake_user.name}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        try:
            db_user = db.query(SQLUser).filter(SQLUser.email == form_data.username).first()

            if db_user is None or not verify_password(form_data.password, db_user.password):
                raise HTTPException(status_code=401, detail="Incorrect name or password", headers={"WWW-Authenticate": "Bearer"})

            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
            # TODO : remove printing the token
            print(f"Access Token: {access_token}")
            return {"access_token": access_token, "token_type": "bearer"}

        except Exception as e:
            # logging.ERROR(f"Login error: {e}")
            raise HTTPException(status_code=500, detail=f"Internal server error, try again later")


@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_fake_current_user) if DISABLE_AUTH else Depends(get_current_user)):
    return current_user

@router.get("/all", response_model=List[User])
async def read_users(db: Session = Depends(get_db)):
    users = db.query(SQLUser).all()
    return users

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(SQLUser).filter(SQLUser.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user