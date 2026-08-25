from pydantic import BaseModel, EmailStr
from datetime import datetime
from models.domain.workspace import WorkspaceType

class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_admin: bool = False

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str

class UserResponse(BaseModel):
    name: str
    user_id: int
    email: EmailStr
    is_admin: bool

class LocationCreateRequest(BaseModel):
    city: str
    street: str
    building: int

class LocationResponse(BaseModel):
    location_id: int
    city: str
    street: str
    building: int


class BookingCreateRequest(BaseModel):
    workspace_id:int
    from_time: datetime
    to_time: datetime
    

class BookingResponse(BaseModel):
    booking_id: int
    workspace_id:int
    from_time: datetime
    to_time: datetime
    total_price: int
    status: str
    
class WorkspaceCreateRequest(BaseModel):
    name:str
    location_id: int
    tariff_id: int
    workspace_type: WorkspaceType  
    

class WorkspaceResponse(BaseModel):
    workspace_id: int
    name:str
    location_id: int
    tariff_id: int
    workspace_type: WorkspaceType

class TariffCreateRequest(BaseModel):
    hourly_rate: float
    daily_rate: float
    monthly_rate: float

class TariffResponse(BaseModel):
    tariff_id: int
    hourly_rate: float
    daily_rate: float
    monthly_rate: float