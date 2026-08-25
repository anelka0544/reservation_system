from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional

from models.abstractions.interfaces import IUserRepository
from models.domain.user import User
from shared.exceptions import WrongUserEmail

class UserController:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def create_user(self, name:str, mail:str, password:str, is_admin:bool) -> User:
        existing_user = await self.user_repo.get_by_email(mail)
        if existing_user:
            raise WrongUserEmail(f"User with email {mail} already exists")
        
        hashed_password = generate_password_hash(password)
        new_user = User(mail=mail, name=name, hash_password=hashed_password, is_admin=is_admin)
        saved_user = await self.user_repo.create(new_user)
        return saved_user
    
    async def authenticate_user(self, mail: str, password: str) -> Optional[User]:
        user = await self.user_repo.get_by_email(mail)
        if not user:
            return None
        if check_password_hash(user.hash_password, password):
            return user
        return None
    
    async def get_all(self)-> list[User]:
        return await self.user_repo.get_all()
    
    async def get_by_id(self, id:int):
        return await self.user_repo.get_by_id(id)

