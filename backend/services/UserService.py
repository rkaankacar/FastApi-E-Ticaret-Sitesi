from backend.repository.IBaseRepository import IBaseRepository # SOYUT ARACILIK NESNESİNİ import edin
from backend.models.entities.Users import Users
from backend.schemas.user_schemas import UserCreate, UserUpdate

# Model ve Schema tiplerini User'a göre belirten bir tip oluşturuluyor
UserRepoType = IBaseRepository[Users, UserCreate, UserUpdate]

class UserService:
    
    def __init__(self, user_repo: UserRepoType):
        self.user_repo = user_repo  
        
    async def get_users_list(self, skip: int = 0, limit: int = 100):
        users = await self.user_repo.get_all(skip=skip, limit=limit)
        return users
    
    async def get_user_by_id(self, user_id: int):
        user = await self.user_repo.get_by_id(user_id)
        return user
    async def create_user(self, user_in: UserCreate):
        new_user = await self.user_repo.create(obj_in=user_in)
        return new_user
    async def update_user(self, user_id: int, user_in: UserUpdate):
        db_user = await self.user_repo.get_by_id(user_id)
        if not db_user:
            return None
        updated_user = await self.user_repo.update(db_obj=db_user, obj_in=user_in)
        return updated_user
    async def delete_user(self, user_id: int):
        deleted_user = await self.user_repo.delete(id=user_id)
        return deleted_user
    
        