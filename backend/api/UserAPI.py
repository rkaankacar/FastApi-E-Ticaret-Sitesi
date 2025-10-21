

from typing import Annotated 
from fastapi import APIRouter, Depends, HTTPException, status
from backend.dependencies.generic_factory import create_repository_dependency, create_service_dependency
from backend.repository.Impl.BaseRepository import BaseRepository 
from backend.services.UserService import UserService
from backend.schemas.user_schemas import UserCreate
from backend.models.entities.Users import Users 


# --- 1. APIRouter Tanımı ---
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# --- 2. JENERİK BAĞIMLILIK ZİNCİRİNİ KURMA ---

# BaseRepository'yi somut model (Users) ile Factory'ye gönderiyoruz.
user_repo_dep = create_repository_dependency(
    repository_class=BaseRepository,
    model_class=Users # <-- User modelini gönderiyoruz
) 

UserDep = create_service_dependency(
    service_class=UserService,
    repository_dependency=user_repo_dep 
)

UserServiceDep = Annotated[UserService, Depends(UserDep)] 

# --- 3. ROUTE TANIMI ---

@router.post(
    "/Create",
    response_model=dict, 
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_in: UserCreate, 
    user_service: UserServiceDep 
):
    user = await user_service.create_user(user_in) 
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User could not be created (e.g., email already exists)."
        )
        
    return {"message": "User created successfully", "user_id": user.UserID}