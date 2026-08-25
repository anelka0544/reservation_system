from datetime import datetime

from models.domain.booking import Booking
from models.abstractions.interfaces import IBookingRepository, IWorkspaceRepository, IUserRepository, ITariffRepository
from shared.exceptions import WorkspaceAlreadyBookedError, InvalidTimeError, WorkspaceNotFound, UserNotFound
from controllers.pricing import PriceCalculator

class BookingController:
    def __init__(self, booking_repo: IBookingRepository, workspace_repo: IWorkspaceRepository, price_calculator: PriceCalculator, user_repo: IUserRepository, tariff_repo: ITariffRepository):
        self.booking_repo = booking_repo
        self.workspace_repo = workspace_repo
        self.price_calculator = price_calculator
        self.user_repo = user_repo
        self.tariff_repo = tariff_repo

    async def create_booking(self, user_id: int, workspace_id: int, start_time: datetime, end_time: datetime) -> Booking:
        if end_time <= start_time:
            raise InvalidTimeError("Время окончания должно быть позже начала.")

        is_free = await self.booking_repo.is_workspace_available(workspace_id, start_time, end_time)
        
        if not is_free:
            raise WorkspaceAlreadyBookedError(f"Место {workspace_id} уже занято на это время.")

        workspace = await self.workspace_repo.get_by_id(workspace_id)

        if workspace is None:
            raise WorkspaceNotFound(f"Место {workspace_id} не найдено")
        
        if await self.user_repo.get_by_id(user_id) is None:
            raise UserNotFound(f"User with id {user_id} not found")
        
        duration = end_time - start_time

        tariff = await self.tariff_repo.get_by_id(workspace.tariff_id)
        total_price = self.price_calculator.calculate_price(tariff, duration)

        new_booking = Booking(
            user_id=user_id,
            workspace_id=workspace_id,
            from_time=start_time,
            to_time=end_time,
            total_price=total_price,
            status="Active"
        )

        saved_booking = await self.booking_repo.create(new_booking)

        return saved_booking
    
    async def cancel_booking(self, booking_id: int, user_id: int):
        booking = await self.booking_repo.get_by_id(booking_id)
        if booking and booking.user_id == user_id:
            booking.status = 'Cancelled'
            await self.booking_repo.update(booking) 
            return True
        return False
    
    async def get_all_bookings(self)->list[Booking]:
        return await self.booking_repo.get_all()
        