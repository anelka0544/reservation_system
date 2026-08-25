from enum import Enum

class Workspace:
    def __init__(self, name: str, location_id: int, tariff_id: int, workspace_type: WorkspaceType, workspace_id: int|None = None):
        self.name = name
        self.location_id = location_id
        self.workspace_id = workspace_id
        self.tariff_id = tariff_id
        self.workspace_type = workspace_type

class WorkspaceType(Enum):
    DESK = "desk"          
    MEETING_ROOM = "meeting_room" 
    OFFICE = "office"    

    def __str__(self):
        return self.value
