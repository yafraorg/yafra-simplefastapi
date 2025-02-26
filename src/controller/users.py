from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from models import User
from database import get_db

router = APIRouter()


# Create a new user
@router.post("/users/", response_model=User)
async def create_user(user: User, db: AsyncSession = Depends(get_db)):
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# Get a list of all users
@router.get("/users/", response_model=List[User])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()


# Get a user by ID
@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update a user by ID
@router.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: int, updated_user: User, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated_user.dict().items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user


# Delete a user by ID
@router.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return user
