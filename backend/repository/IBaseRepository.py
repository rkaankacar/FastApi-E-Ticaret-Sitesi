from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from backend.core.base import Base
ModelType = TypeVar("ModelType", bound=Base) # type: ignore
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
class IBaseRepository(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    __slots__ = ("__weakref__",)
    @abstractmethod
    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        pass

    @abstractmethod
    async def get_all(self, *,skip:int, limit:int) -> List[ModelType]:
        pass

    @abstractmethod
    async def create(self,*, obj_in: CreateSchemaType) -> ModelType:
        pass

    @abstractmethod
    async def update(self, *,db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        pass

    @abstractmethod
    async def delete(self, *, id: Any) -> ModelType:
        pass