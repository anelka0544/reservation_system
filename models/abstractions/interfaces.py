from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from models.domain.booking import Booking
from models.domain.workspace import Workspace, WorkspaceType
from models.domain.user import User
from models.domain.location import Location
from models.domain.tariff import Tariff

class IBookingRepository(ABC):
    @abstractmethod
    async def is_workspace_available(self, workspace_id: int, start: datetime, end: datetime) -> bool:
        pass 

    @abstractmethod
    async def create(self, Booking: Booking) -> Booking:
        pass

    @abstractmethod
    async def get_all(self) -> list[Booking]:
        pass

    @abstractmethod
    async def get_by_id(self, booking_id: int) -> Booking | None:
        pass

    @abstractmethod
    async def update(self, booking: Booking) -> Booking | None:
        pass

    @abstractmethod
    async def delete(self, booking_id: int) -> bool:
        pass

class IWorkspaceRepository(ABC):
    @abstractmethod
    async def get_by_id(self, workspace_id: int) -> Workspace:
        pass 

    @abstractmethod
    async def get_workspaces_by_location(self, location_id: int, workspace_type: Optional[WorkspaceType] = None) -> list[Workspace]:
        pass 

    @abstractmethod
    async def create(self, workspace: Workspace) -> Workspace:
        pass

    @abstractmethod
    async def get_all(self) -> list[Workspace]:
        pass

    @abstractmethod
    async def update(self, workspace: Workspace) -> Workspace | None:
        pass

    @abstractmethod
    async def delete(self, workspace_id: int) -> bool:
        pass

class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass
        
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def update(self, user: User) -> User | None:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        pass

class ILocationRepository(ABC):
    @abstractmethod
    async def create(self, location: Location) -> Location:
        pass
        
    @abstractmethod
    async def get_all(self) -> list[Location]:
        pass

    @abstractmethod
    async def get_by_id(self, location_id: int) -> Location | None:
        pass

    @abstractmethod
    async def update(self, location: Location) -> Location | None:
        pass

    @abstractmethod
    async def delete(self, location_id: int) -> bool:
        pass

class ITariffRepository(ABC):
    @abstractmethod
    async def create(self, tariff: Tariff) -> Tariff:
        pass
    
    @abstractmethod
    async def get_by_id(self, tariff_id: int) -> Tariff | None:
        pass

    @abstractmethod
    async def update(self, tariff: Tariff) -> Tariff | None:
        pass

    @abstractmethod
    async def delete(self, tariff_id: int) -> bool:
        pass