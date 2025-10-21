from typing import Generic, Type, List, Optional, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Senin tanımladığın IBaseRepository'den gelen tipler
# Artık ModelType, CreateSchemaType, UpdateSchemaType birer TypeVar
from backend.repository import (
    IBaseRepository, ModelType, CreateSchemaType, UpdateSchemaType
)

# Bu sınıf IBaseRepository'den miras alıp, tüm soyut metotları uygular.
class BaseRepository(IBaseRepository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    
    # Not: IBaseRepository'den miras aldığımız için,
    # bu sınıfın tüm metotları (get_by_id, create, vb.) zorunludur.
    
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        # Model, Repository'nin hangi DB tablosuyla çalışacağını belirtir.
        self.model = model
        self.db = db_session

    async def get_by_id(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()

    async def get_all(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        # Pydantic v2 için doğru kullanım: model_dump()
        obj_in_data = obj_in.model_dump() 
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj) # Yeni oluşan ID'yi/Alanları geri almak için
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = db_obj.__dict__
        
        # Düzeltildi: obj_in.model_dump() kullanılır
        update_data = obj_in.model_dump(exclude_unset=True) 
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
                
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: Any) -> ModelType:
        obj = await self.get_by_id(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj