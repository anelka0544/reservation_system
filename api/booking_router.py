from models.dto import BookingCreateRequest, BookingResponse
from api.dependencies import BookingController, get_booking_controller
from shared.security import security
from fastapi import APIRouter, Depends, HTTPException
from shared.auth import get_current_user, require_admin
from shared.exceptions import WorkspaceAlreadyBookedError, InvalidTimeError, WorkspaceNotFound, UserNotFound


router = APIRouter(prefix="/book", tags=["Bookings"])

@router.get("/", response_model=list[BookingResponse])
async def get_bookings(controller: BookingController = Depends(get_booking_controller), _ = Depends(require_admin)):
    bookings = await controller.get_all_bookings()
    return bookings

@router.post("/create", response_model=BookingResponse)
async def register(request: BookingCreateRequest, controller: BookingController = Depends(get_booking_controller), curr_user = Depends(get_current_user)):
    try:
        start_ = request.from_time.replace(tzinfo=None)
        end_ = request.to_time.replace(tzinfo=None)
        booking = await controller.create_booking(user_id=curr_user.user_id, workspace_id=request.workspace_id, start_time=start_, end_time=end_)
        return BookingResponse(booking_id = booking.booking_id, user_id=curr_user.user_id, workspace_id=booking.workspace_id, from_time=booking.from_time, to_time=booking.to_time, status=booking.status, total_price=booking.total_price)
    except WorkspaceAlreadyBookedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except WorkspaceNotFound as e:
        raise HTTPException(status_code=404, detail=str(e)) 
    except InvalidTimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))