

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, text 
from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator 


# --- Ayarlar ---
YENI_SCHEMA_ADI = "saat_satis"



ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:2004@localhost:5432/clockdatabase" 

# --- SQLAlchemy Ayarları ---

metadata_obj = MetaData(schema=YENI_SCHEMA_ADI)


async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True, 
)

# 2. Asenkron Oturum Fabrikası (Session Maker)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

Base = declarative_base(metadata=metadata_obj)


async def create_db_and_tables(engine: AsyncEngine, schema_name: str, base_metadata: MetaData):
    print(">>> [LIFESPAN] Veritabanı kurulumu başlatıldı...")
    
    try:
        # 1. Şemayı oluştur
        async with engine.begin() as conn:
            # PostgreSQL'de şemayı oluştur
            await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
            
            # Tabloları oluşturma işlemini senkron olarak çalıştır ve TAMAMLANMASINI BEKLE
            await conn.run_sync(base_metadata.create_all) 
            
        print(">>> [LIFESPAN] Veritabanı tabloları başarıyla kuruldu.")
        
    except Exception as e:
        # Hata mesajını konsola bas!
        print("!!! [HATA] Veritabanı kurulumunda bir sorun oluştu.")
        print(f"!!! Hata Detayı: {e}")


# 3. Asenkron Veritabanı Bağımlılığı (Dependency)

async def gt_db() -> AsyncGenerator[AsyncSession, None]: 
    async with AsyncSessionLocal() as session: 
        try:
            yield session
        except Exception:
            await session.rollback() 
            raise
        finally:
            await session.close()