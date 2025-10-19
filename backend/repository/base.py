from typing import Any, Generic, Type, TypeVar, List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase

# SQLAlchemy model tipini temsil etmek için
ModelType = TypeVar("ModelType", bound=DeclarativeBase) 
# Pydantic create şemasını temsil etmek için
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# Pydantic update şemasını temsil etmek için
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        
    