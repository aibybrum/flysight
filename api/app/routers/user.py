from typing import List
from fastapi import APIRouter, Depends

from api.app.services.user import UserService
from api.app.schemas.user import User, UserCreate
from api.app.utils.service_result import handle_result
from api.app.config.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[User])
async def get_users(db: get_db = Depends()):
    result = UserService(db).get_users()
    return handle_result(result)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: get_db = Depends()):
    result = UserService(db).get_user(user_id)
    return handle_result(result)


@router.post("", response_model=User)
async def create_user(user: UserCreate, db: get_db = Depends()):
    result = UserService(db).create_user(user)
    return handle_result(result)


@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: int, db: get_db = Depends()):
    result = UserService(db).delete_user(user_id)
    return handle_result(result)


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: User, db: get_db = Depends()):
    result = UserService(db).update_user(user_id, user)
    return handle_result(result)




