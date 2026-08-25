from models.dto import TariffCreateRequest, TariffResponse
from api.dependencies import TariffController, get_tariff_controller
from shared.security import security
from fastapi import APIRouter, Depends, HTTPException
from shared.auth import get_current_user, require_admin
from shared.exceptions import LocationNotFoundError

router = APIRouter(prefix="/tariffs", tags=["Tariffs"])

@router.post("/create", response_model=TariffResponse)
async def register(request: TariffCreateRequest, controller: TariffController = Depends(get_tariff_controller), _ = Depends(require_admin)):
    tr = await controller.create_tariff(hourly_rate=request.hourly_rate, daily_rate=request.daily_rate, monthly_rate=request.monthly_rate)
    return TariffResponse(monthly_rate=tr.monthly_rate, tariff_id=tr.tariff_id, hourly_rate=tr.hourly_rate, daily_rate=tr.daily_rate)

    
@router.get("/", response_model=list[TariffResponse])
async def get_tariffs(controller: TariffController = Depends(get_tariff_controller), _ = Depends(require_admin)):
    tariffs = await controller.get_all_()
    return tariffs

