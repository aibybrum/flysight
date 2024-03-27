from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.schemas.landing import Landing
from app.services.jump.landing import LandingService
from app.utils.service_result import handle_result

router = APIRouter(
    prefix="/landings",
    tags=["Landing"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{jump_id}", response_model=Landing)
async def get_landings(jump_id: UUID):
    result = LandingService(jump_id).get_landing()
    return handle_result(result)
