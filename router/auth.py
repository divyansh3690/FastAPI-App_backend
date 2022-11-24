import sys

sys.path.append("..")

from datetime import timedelta, datetime
from typing import Optional
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from starlette import status
from database import Base, SessionLocal, engine
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException
import model

SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
model.Base.metadata.create_all(bind=engine)


class ui_user(BaseModel):
    username: str = Field(default=None)
    password: str = Field(default=None)
    name: str = Field(default=None)
    age: int = Field(default=None)

    class Config: {
        "user_demo": {
            "username": "Divyansh3690",
            "password": "pass",
            "name": "Divyansh",
            "age": 19
        }
    }


router = APIRouter(
    prefix="/authentication",
    responses={404: {"description": "Not found"}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


becrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def pass_hash_converter(password):
    return becrypt_context.hash(password)


def verify_password(password, hashed_password):
    return becrypt_context.verify(password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(model.Users). \
        filter(model.Users.username == username) \
        .first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()


def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/newuser", tags=["users"])
async def create_newuser(newuser: ui_user, db: Session = Depends(get_db)):
    user_model = model.Users()
    user_model.username = newuser.username
    hashed_pass = pass_hash_converter(newuser.password)
    user_model.password = hashed_pass
    user_model.name = newuser.name
    user_model.age = newuser.age
    db.add(user_model)
    db.commit()
    return {
        "result": "Successful",
        "new user": "added"
    }


@router.post("/token", tags=["users"])
async def get_token(formdata: OAuth2PasswordRequestForm = Depends(),
                    db: Session = Depends(get_db)):
    user = authenticate_user(formdata.username, formdata.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    return {"token": token}


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response


def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception
