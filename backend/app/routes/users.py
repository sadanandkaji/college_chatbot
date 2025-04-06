from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.schemas import UserCreate, UserResponse
from app.db import models
from passlib.hash import bcrypt
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await db.scalar(
        select(models.User).where(models.User.email == user.email)
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
    username=user.username,
    email=user.email,
    hashed_password=bcrypt.hash(user.password)
)


    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await db.scalar(
        select(models.User).where(models.User.email == user.email)
    )
    if not db_user or not bcrypt.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = jwt.encode({"sub": db_user.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
