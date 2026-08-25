from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from shared.security import security
from api.dependencies import get_user_controller

token_auth_scheme = HTTPBearer()

async def get_current_user(swagger_token = Depends(token_auth_scheme), payload = Depends(security.access_token_required), user_controller = Depends(get_user_controller)):
    user_id = payload.sub 
    user = await user_controller.get_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def require_admin(current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")
    return current_user