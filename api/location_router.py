from models.dto import LocationCreateRequest, LocationResponse
from api.dependencies import LocationController, get_location_controller
from shared.security import security
from fastapi import APIRouter, Depends, HTTPException
from shared.auth import get_current_user, require_admin
from shared.exceptions import LocationNotFoundError

router = APIRouter(prefix="/location", tags=["Location"])

@router.post("/create", response_model=LocationResponse)
async def register(request: LocationCreateRequest, controller: LocationController = Depends(get_location_controller), _ = Depends(require_admin)):
    location = await controller.create_location(city=request.city, street=request.street, building=request.building)
    return LocationResponse(city=location.city, location_id=location.location_id, street=location.street, building=location.building)

    
@router.get("/", response_model=list[LocationResponse])
async def get_locations(controller: LocationController = Depends(get_location_controller), _ = Depends(get_current_user)):
    locations = await controller.get_all_locations()
    return locations

@router.get("/stats")
async def get_locations_stats(location_id: int, controller: LocationController = Depends(get_location_controller), _ = Depends(get_current_user)):
    try:
        stats = await controller.get_location_load_stats(location_id)
        return stats
    except LocationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


