from fastapi import APIRouter, HTTPException
from uuid import UUID
from api.app.config.influxdb import client, bucket
from api.app.schemas.landing import Landing
from api.app.services.landing import LandingService

router = APIRouter(
    prefix="/landings",
    tags=["Landing"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{jump_id}", response_model=Landing)
async def get_landings(jump_id: UUID):
    db_landing = LandingService(bucket, client).get_landing(jump_id)
    if db_landing is None:
        raise HTTPException(status_code=404, detail="Jump not found")
    return db_landing
