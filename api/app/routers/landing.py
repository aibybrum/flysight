from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends

from app.schemas.landing import Landing
from app.services.landing.landing_service import LandingService
from app.utils.service_result import handle_result
from app.dependencies import get_landing_service

router = APIRouter(
    prefix="/landings",
    tags=["Landing"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{jump_id}", response_model=Landing)
async def get_landings(jump_id: UUID, landing_service: LandingService = Depends(get_landing_service)):
    result = landing_service.get_landing(jump_id)
    return handle_result(result)
