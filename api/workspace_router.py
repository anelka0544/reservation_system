from models.dto import WorkspaceCreateRequest, WorkspaceResponse
from api.dependencies import WorkspaceController, get_workspace_controller
from shared.security import security
from fastapi import APIRouter, Depends, HTTPException, Query
from shared.auth import get_current_user, require_admin
from datetime import datetime
from typing import Optional
from models.domain.workspace import WorkspaceType
from shared.exceptions import WorkspaceNotFound, LocationNotFoundError, TariffNotFoundError, InvalidTimeError

router = APIRouter(prefix="/spaces", tags=["Workspaces"])

@router.get("/all", response_model=list[WorkspaceResponse])
async def get_bookings(controller: WorkspaceController = Depends(get_workspace_controller), _ = Depends(require_admin)):
    workspaces = await controller.get_all_workspaces()
    return workspaces

@router.post("/create", response_model=WorkspaceResponse)
async def register(request: WorkspaceCreateRequest, controller: WorkspaceController = Depends(get_workspace_controller), _ = Depends(require_admin)):
    try:
        workspace = await controller.create_workspace(name=request.name, location_id=request.location_id, tariff_id = request.tariff_id, workspace_type=request.workspace_type)
        return WorkspaceResponse(workspace_id=workspace.workspace_id, name=workspace.name, location_id=workspace.location_id, tariff_id = workspace.tariff_id, workspace_type=workspace.workspace_type)
    except LocationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TariffNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/location/{location_id}", response_model=list[WorkspaceResponse])
async def get_workspaces_by_location(location_id: int, workspace_type: Optional[str] = Query(None, description="Filter by workspace type"), controller: WorkspaceController = Depends(get_workspace_controller), current_user = Depends(get_current_user)):
    workspace_type_enum = None
    if workspace_type:
        try:
            workspace_type_enum = WorkspaceType(workspace_type)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid workspace type: {workspace_type}")
    try:
        workspaces = await controller.get_workspaces_by_location(location_id, workspace_type_enum)
    except LocationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return workspaces

@router.get("/available", response_model=list[WorkspaceResponse])
async def get_available_workspaces(location_id: int, start_time: datetime, end_time: datetime, controller: WorkspaceController = Depends(get_workspace_controller), current_user = Depends(get_current_user)):
    start_ = start_time.replace(tzinfo=None)
    end_ = end_time.replace(tzinfo=None)
    if start_ >= end_:
        raise HTTPException(status_code=400, detail="start_time must be before end_time")
    
    if start_ < datetime.now():
        raise HTTPException(status_code=400, detail="start_time cannot be in the past")
    
    try:
        workspaces = await controller.get_available_workspaces(location_id=location_id, start_time=start_, end_time=end_)
    except InvalidTimeError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except LocationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    
    if not workspaces:
        raise HTTPException(status_code=404, detail="No available workspaces found for the selected time period")
    
    return workspaces

@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace_by_id(workspace_id: int, controller: WorkspaceController = Depends(get_workspace_controller), current_user = Depends(get_current_user)):
    workspace = await controller.workspace_repo.get_by_id(workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    return WorkspaceResponse(workspace_id=workspace.workspace_id, name=workspace.name, location_id=workspace.location_id, tariff_id=workspace.tariff_id, workspace_type=workspace.workspace_type)

@router.put("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(workspace_id: int, request: WorkspaceCreateRequest, controller: WorkspaceController = Depends(get_workspace_controller), _ = Depends(require_admin)):
    try:
        workspace = await controller.update_workspace(workspace_id=workspace_id, name=request.name, location_id=request.location_id, tariff_id=request.tariff_id, workspace_type=request.workspace_type)
        return WorkspaceResponse(workspace_id=workspace.workspace_id, name=workspace.name, location_id=workspace.location_id, tariff_id=workspace.tariff_id, workspace_type=workspace.workspace_type)
    except WorkspaceNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except LocationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TariffNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{workspace_id}")
async def delete_workspace(workspace_id: int, controller: WorkspaceController = Depends(get_workspace_controller), _ = Depends(require_admin)):
    try:
        await controller.delete_workspace(workspace_id)
        return {"message": "Workspace deleted successfully"}
    except WorkspaceNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))