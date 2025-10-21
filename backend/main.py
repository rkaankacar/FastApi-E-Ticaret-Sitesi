

from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager # Lifespan için gerekli

# base.py'den Lifespan için gerekli objeleri ve fonksiyonu import ediyoruz
from backend.core.base import (
    async_engine, 
    Base, 
    YENI_SCHEMA_ADI, 
    create_db_and_tables # Yeni eklediğimiz fonksiyon
) 

from backend.api.UserAPI import router 

from backend.models.entities.Users import Users 
from backend.models.entities.Orders import Orders 
from backend.models.entities.OrdersDetails import OrdersDetails 
from backend.models.entities.Brands import Brands
from backend.models.entities.Cart import Cart
from backend.models.entities.Reviews import Reviews
from backend.models.entities.Watches_Images import Watches_Images
from backend.models.entities.Watches import Watches

# --- LIFESPAN YÖNETİCİSİ ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Uygulama Başlatılırken Çalışır (Startup)
    print(">>> [APP STARTUP] Veritabanı kurulum kontrolü başlatılıyor...")
    try:
        # Tablo oluşturma fonksiyonunu çağır
        await create_db_and_tables(
            engine=async_engine,
            schema_name=YENI_SCHEMA_ADI,
            base_metadata=Base.metadata
        )
        print(">>> [APP STARTUP] Kurulum tamamlandı. Uygulama başlatılıyor.")
        yield
    finally:
        # Uygulama Kapatılırken Çalışır (Shutdown)
        print(">>> [APP SHUTDOWN] Uygulama kapatılıyor.")


# --- FASTAPI UYGULAMASI ---
# Lifespan olayını FastAPI'ye tanımlıyoruz
app = FastAPI(lifespan=lifespan) 

app.include_router(router) # UserAPI'den alınan router'ı FastAPI uygulamasına dahil eder.
