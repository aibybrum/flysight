from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.dependencies import get_user_service
from app.services.user.user_service import UserService
from app.utils.service_result import handle_result
from app.schemas.user import User, UserCreate, UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[User])
async def get_users(user_service: UserService = Depends(get_user_service)):
    result = user_service.get_users()
    return handle_result(result)


# @router.get("/{user_id}", response_model=User)
# async def get_user(user_id: UUID, user_service: UserService = Depends(get_user_service)):
#     result = user_service.get_user(user_id)
#     return handle_result(result)


@router.post("", response_model=User)
async def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    result = user_service.create_user(user)
    return handle_result(result)


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, user_service: UserService = Depends(get_user_service)):
    result = user_service.delete_user(user_id)
    return handle_result(result)


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: UUID, user: UserUpdate, user_service: UserService = Depends(get_user_service)):
    result = user_service.update_user(user_id, user)
    return handle_result(result)
    