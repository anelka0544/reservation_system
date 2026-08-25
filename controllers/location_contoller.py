from datetime import datetime
from models.abstractions.interfaces import ILocationRepository, IWorkspaceRepository, IBookingRepository
from models.domain.location import Location
from shared.exceptions import LocationNotFoundError

class LocationController:
    def __init__(self, location_repo: ILocationRepository, workspace_repo: IWorkspaceRepository, booking_repo: IBookingRepository):
        self.location_repo = location_repo
        self.workspace_repo = workspace_repo
        self.booking_repo = booking_repo

    async def create_location(self, city: str, street:str, building:int) -> Location:
        new_location = Location(city=city, street=street, building=building)
        saved_location = await self.location_repo.create(new_location)
        return saved_location
    
    async def get_all_locations(self) -> list[Location]:
        return await self.location_repo.get_all()
    
    async def get_location_load_stats(self, location_id: int) -> dict:
        current_time = datetime.now()

        loc = await self.location_repo.get_by_id(location_id)
        if not loc:
            raise LocationNotFoundError(f"Location with id {location_id} not found")

        workspaces_in_location = await self.workspace_repo.get_workspaces_by_location(location_id)
        total_workspaces = len(workspaces_in_location)

        if total_workspaces == 0:
            return {"total": 0, "occupied": 0, "load_percentage": 0}

        occupied_count = 0
        for ws in workspaces_in_location:
            #print("234", ws.workspace_id)
            if not await self.booking_repo.is_workspace_available(ws.workspace_id, current_time, current_time):
                occupied_count += 1

        total_workspaces = len(workspaces_in_location)

        load_percentage = (occupied_count / total_workspaces) * 100

        return {"total_places": total_workspaces, "occupied_places": occupied_count, "load_percentage": round(load_percentage, 2)}

