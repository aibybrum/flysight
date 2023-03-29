from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.services.user import UserService
from app.schemas.user import User, UserCreate, UserUpdate
from app.config.postgres import get_db

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[User])
async def get_users(db: get_db = Depends()):
    db_users = UserService(db).get_users()
    return db_users


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: UUID, db: get_db = Depends()):
    db_user = UserService(db).get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("", response_model=User)
async def create_user(user: UserCreate, db: get_db = Depends()):
    if UserService(db).check_username(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    db_user = UserService(db).create_user(user)
    if not db_user:
        return HTTPException(status_code=500)
    return db_user


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, db: get_db = Depends()):
    db_user = UserService(db).get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        UserService(db).delete_user(user_id)
    except (Exception,):
        raise HTTPException(status_code=304)
    return {"message": "User deleted successfully"}


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: UUID, user: UserUpdate, db: get_db = Depends()):
    db_user = UserService(db).get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        UserService(db).update_user(user_id, user)
    except (Exception,):
        raise HTTPException(status_code=304)
    return db_user
