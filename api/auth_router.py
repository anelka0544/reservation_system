from models.dto import UserLoginRequest, TokenResponse, UserRegisterRequest, UserResponse
from api.dependencies import UserController, get_user_controller
from shared.security import security
from fastapi import APIRouter, Depends, HTTPException
from shared.exceptions import WrongUserEmail

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register(request: UserRegisterRequest, controller: UserController = Depends(get_user_controller)):
    try:
        user = await controller.create_user(name = request.name, mail=request.email, password=request.password, is_admin=request.is_admin)
        return UserResponse(name = user.name, user_id=user.user_id, email=user.mail, is_admin=user.is_admin)
    except WrongUserEmail as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model = TokenResponse)
async def login(creds: UserLoginRequest, controller: UserController = Depends(get_user_controller)):
    user = await controller.authenticate_user(creds.email, creds.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = security.create_access_token(uid=str(user.user_id))
    
    return TokenResponse(access_token=token)

