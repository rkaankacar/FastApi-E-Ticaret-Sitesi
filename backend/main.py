from fastapi import FastAPI, Depends
from backend.core.base import gt_db  
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select

from backend.models.entities.Users import Users # Users.py dosyasından Users sınıfını içe aktarır
from backend.models.entities.Orders import Orders # Orders.py dosyasından Orders sınıfını içe aktarır
from backend.models.entities.OrdersDetails import OrdersDetails # OrdersDetails.py dosyasından OrdersDetails sınıfını içe aktarır
from backend.models.entities.Brands import Brands
from backend.models.entities.Cart import Cart
from backend.models.entities.Reviews import Reviews
from backend.models.entities.Watches_Images import Watches_Images
from backend.models.entities.Watches import Watches


app = FastAPI() # FastAPI uygulamasının ana örneği oluşturulur.

@app.get("/") # Kök URL'ye (/) gelen GET istekleri için yol tanımlayıcı (endpoint).
async def root(): # Asenkron fonksiyon olarak tanımlanır.
    return {"message": "Hello, World!"} # Basit bir JSON yanıtı döndürülür.

@app.get("/db-test/") # Veritabanı testi için bir yol tanımlayıcı.
# db parametresi, Depends(gt_db) ile Asenkron Oturum (AsyncSession) alır.
async def db_test(db: AsyncSession = Depends(gt_db)): 
    
    # SQLAlchemy 2.0 stilinde asenkron sorgu: Users modelindeki tüm kayıtları seçer.
    result = await db.execute(select(Users)) 
    
    # Sorgu sonuçları scalar() ile ORM nesnesi olarak alınır ve listeye dönüştürülür.
    users = result.scalars().all() 
    
    # Kullanıcı adları listesini içeren JSON yanıtı döndürülür.
    return {"users": [user.FullName for user in users]}