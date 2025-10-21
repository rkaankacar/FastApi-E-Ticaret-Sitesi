

from typing import Generic, Type, List, Optional, Any
from sqlalchemy import select, delete 
from sqlalchemy.ext.asyncio import AsyncSession



from backend.repository.IBaseRepository import ( 
    IBaseRepository, ModelType, CreateSchemaType, UpdateSchemaType
)


class BaseRepository(IBaseRepository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self.model = model
        
        self.db = db_session 

    async def get_by_id(self, id: Any) -> Optional[ModelType]:
       
        result = await self.db.execute(select(self.model).where(self.model.id == id)) 
        return result.scalars().first()

    async def get_all(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        
        result = await self.db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump() 
        db_obj = self.model(**obj_in_data)
        
      
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj) 
        return db_obj

    async def update(self, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        
        update_data = obj_in.model_dump(exclude_unset=True) 
        
       
        for field, value in update_data.items():
            setattr(db_obj, field, value)
                
        
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, *, id: Any) -> ModelType:
        
        obj = await self.get_by_id(id) 
        
        if obj:
           
            await self.db.delete(obj) 
            await self.db.commit()
            
       
        return obj 