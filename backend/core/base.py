from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator # Artık asenkron jeneratör kullanıyoruz

# --- Ayarlar ---
YENI_SCHEMA_ADI = "saat_satis"


# PostgreSQL için: 'postgresql+psycopg2://' yerine 'postgresql+asyncpg://' kullanılır.
ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:2004@localhost:5432/clockdatabase" 

# --- SQLAlchemy Ayarları ---

metadata_obj = MetaData(schema=YENI_SCHEMA_ADI)


async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True, # SQL sorgularını görmek için True yapabilirsiniz
)

# 2. Asenkron Oturum Fabrikası (Session Maker)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession, # Asenkron oturum sınıfını kullan
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

Base = declarative_base(metadata=metadata_obj)


# 3. Asenkron Veritabanı Bağımlılığı (Dependency)

async def gt_db() -> AsyncGenerator[AsyncSession, None]: 
    async with AsyncSessionLocal() as session: # Doğru ASYNC context manager kullanımı
        try:
            yield session
        except Exception:
            await session.rollback() # Hata durumunda rollback yap
            raise
        finally:
            await session.close() # Oturumu asenkron olarak kapat