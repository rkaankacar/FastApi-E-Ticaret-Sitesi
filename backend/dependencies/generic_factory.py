

from typing import TypeVar, Type, Any, Callable, AsyncGenerator 
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Kendi temel sınıflarınızın importları
from backend.repository.IBaseRepository import IBaseRepository 
from backend.core.base import gt_db # Sizin DB bağımlılık adınız

# --- JENERİK TİPLER ---
RepositoryType = TypeVar("RepositoryType", bound=IBaseRepository)
ServiceType = TypeVar("ServiceType", bound=Any) 

# --- 1. REPOSITORY FACTORY (En Alt Katman) ---

def create_repository_dependency(
    repository_class: Type[RepositoryType],
    model_class: Type[Any] # <-- Yeni: Model sınıfını bekliyoruz
) -> Callable[[AsyncSession], IBaseRepository]: 
    
    async def _get_repo(session: AsyncSession = Depends(gt_db)) -> IBaseRepository:
        # Repository'nin beklediği 'db_session' ve 'model' argümanları gönderildi.
        return repository_class(db_session=session, model=model_class)
        
    return _get_repo


# --- 2. SERVICE FACTORY (API Katmanına En Yakın) ---

def create_service_dependency(
    service_class: Type[ServiceType],
    repository_dependency: Callable[..., Any] 
) -> Callable[[IBaseRepository], AsyncGenerator[ServiceType, None]]:
    
    async def _get_service(
        repo_instance: IBaseRepository = Depends(repository_dependency)
    ) -> AsyncGenerator[ServiceType, None]: 
        
        yield service_class(user_repo=repo_instance) 
        
    return _get_service