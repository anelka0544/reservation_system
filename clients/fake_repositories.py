from datetime import datetime

from models.abstractions.interfaces import ILocationRepository, IBookingRepository, IUserRepository, IWorkspaceRepository, ITariffRepository
from models.domain.booking import Booking
from models.domain.workspace import Workspace, WorkspaceType
from models.domain.user import User
from models.domain.location import Location
from models.domain.tariff import Tariff

from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class FakeRepository(Generic[T]):
    def __init__(self):
        self._items: List[T] = []
        self._next_id: int = 1

    def get_id(self, item: T) -> int:
        pass

    def _set_id(self, item: T, id_value: int) -> None:
        pass

    async def create(self, item: T) -> T:
        self._set_id(item, self._next_id)
        self._next_id += 1
        self._items.append(item)
        return item

    async def get_by_id(self, id: int) -> Optional[T]:
        for item in self._items:
            if self.get_id(item) == id:
                return item
        return None

    async def get_all(self) -> List[T]:
        return self._items

    async def update(self, item: T) -> Optional[T]:
        item_id = self.get_id(item)
        for i, existing in enumerate(self._items):
            if self.get_id(existing) == item_id:
                self._items[i] = item
                return item
        return None

    async def delete(self, id: int) -> bool:
        for i, item in enumerate(self._items):
            if self.get_id(item) == id:
                self._items.pop(i)
                return True
        return False
    
class FakeBookingRepo(FakeRepository[Booking], IBookingRepository):
    def get_id(self, booking: Booking) -> int:
        return booking.booking_id

    def _set_id(self, booking: Booking, id_value: int) -> None:
        booking.booking_id = id_value

    async def is_workspace_available(self, workspace_id: int, start: datetime, end: datetime) -> bool:
        for booking in self._items:
            if booking.workspace_id == workspace_id and booking.status != 'Cancelled':
                if not (booking.to_time <= start or booking.from_time >= end):
                    return False 
        return True

class FakeWorkspaceRepository(FakeRepository[Workspace], IWorkspaceRepository):
    def get_id(self, workspace: Workspace) -> int:
        return workspace.workspace_id

    def _set_id(self, workspace: Workspace, id_value: int) -> None:
        workspace.workspace_id = id_value

    async def get_workspaces_by_location(self, location_id: int, workspace_type: Optional[WorkspaceType] = None) -> list[Workspace]:
        result = [ws for ws in self._items if ws.location_id == location_id]
        if workspace_type is not None:
            result = [ws for ws in result if ws.workspace_type == workspace_type]
        return result
    
    
class FakeUserRepository(FakeRepository[User], IUserRepository):

    def get_id(self, user: User) -> int:
        return user.user_id

    def _set_id(self, user: User, id_value: int) -> None:
        user.user_id = id_value

    async def get_by_email(self, email: str) -> User | None:
        for user in self._items:
            if user.mail == email:
                return user
        return None
    
class FakeLocationRepository(FakeRepository[Location], ILocationRepository):
    def get_id(self, location: Location) -> int:
        return location.location_id

    def _set_id(self, location: Location, id_value: int) -> None:
        location.location_id = id_value

class FakeTariffRepo(FakeRepository[Tariff], ITariffRepository):
    def get_id(self, item: Tariff) -> int: return item.tariff_id
    def _set_id(self, item: Tariff, id_value: int) -> None: item.tariff_id = id_value