from app.config.postgres import SessionLocal
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.jump.jump_service import JumpService
from app.services.user.user_service import UserService

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

def get_jump_service(user_service: UserService = Depends(get_user_service)) -> JumpService:
    return JumpService(user_service)