from datetime import datetime
from typing import Optional

from models.abstractions.interfaces import IWorkspaceRepository, IBookingRepository, ILocationRepository, ITariffRepository
from models.domain.workspace import Workspace, WorkspaceType
from models.domain.tariff import Tariff
from shared.exceptions import InvalidTimeError, WorkspaceNotFound, LocationNotFoundError, TariffNotFoundError

class WorkspaceController:
    def __init__(self, workspace_repo: IWorkspaceRepository, booking_repo: IBookingRepository, loc_repo: ILocationRepository, t_repo: ITariffRepository):
        self.workspace_repo = workspace_repo
        self.booking_repo = booking_repo
        self.loc_repo = loc_repo
        self.tariff_repo=t_repo

    async def create_workspace(self, name:str, location_id:int, tariff_id:int, workspace_type: WorkspaceType) -> Workspace:
        new_workspace = Workspace(name = name, location_id=location_id, tariff_id=tariff_id, workspace_type=workspace_type)
        loc = await self.loc_repo.get_by_id(location_id)
        if not loc:
            raise LocationNotFoundError(f"Locations with id {location_id} not found")
        
        tr = await self.tariff_repo.get_by_id(tariff_id)
        if not tr:
            raise TariffNotFoundError(f"Tariff with id {tariff_id} not found")
        
        saved_worksapce = await self.workspace_repo.create(new_workspace)
        return saved_worksapce
    
    async def get_all_workspaces(self) -> list[Workspace]:
        return await self.workspace_repo.get_all()

    async def get_available_workspaces(self, location_id: int, start_time: datetime, end_time: datetime) -> list[Workspace]:
        if start_time >= end_time:
            raise InvalidTimeError("start_time must be before end_time")
        if start_time < datetime.now():
            raise InvalidTimeError("start_time cannot be in the past")
        
        loc = await self.loc_repo.get_by_id(location_id)
        if not loc:
            raise LocationNotFoundError(f"Locations with id {location_id} not found")
        
        all_workspaces = await self.workspace_repo.get_workspaces_by_location(location_id)

        available_workspaces = []
        for ws in all_workspaces:
            if await self.booking_repo.is_workspace_available(ws.workspace_id, start_time, end_time):
                available_workspaces.append(ws)

        return available_workspaces
    
    async def get_workspaces_by_location(self, location_id:int, workspace_type: Optional[WorkspaceType] = None) -> list[Workspace]:

        loc = await self.loc_repo.get_by_id(location_id)
        if not loc:
            raise LocationNotFoundError(f"Locations with id {location_id} not found")
        
        return await self.workspace_repo.get_workspaces_by_location(location_id, workspace_type)
    
    async def update_workspace(self, workspace_id: int, name: str, location_id: int, tariff_id: int, workspace_type: WorkspaceType) -> Workspace:
        if await self.workspace_repo.get_by_id(workspace_id) is None:
            raise WorkspaceNotFound(f"Workspace with ID {workspace_id} not found")
        
        loc = await self.loc_repo.get_by_id(location_id)
        if not loc:
            raise LocationNotFoundError(f"Locations with id {location_id} not found")
        
        tr = await self.tariff_repo.get_by_id(tariff_id)
        if not tr:
            raise TariffNotFoundError(f"Tariff with id {tariff_id} not found")
        
        workspace_to_update = Workspace(workspace_id=workspace_id, name=name, location_id=location_id, tariff_id=tariff_id, workspace_type=workspace_type)
        updated_workspace = await self.workspace_repo.update(workspace_to_update)
        return updated_workspace

    async def delete_workspace(self, workspace_id: int) -> bool:
        if await self.workspace_repo.get_by_id(workspace_id) is None:
            raise WorkspaceNotFound(f"Workspace with ID {workspace_id} not found")
        return await self.workspace_repo.delete(workspace_id)