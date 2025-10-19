# create_tables.py

from sqlalchemy import text
from backend.core.base import engine, Base, YENI_SCHEMA_ADI
from backend.models.entities import Brands,Users,Orders,OrdersDetails,Cart,Reviews,Watches,Watches_Images


print(f"Veritabanı motoru başlatıldı: {engine.url}")

# Şemayı manuel olarak oluşturmak iyi bir pratiktir, bu kalsın.
print(f"'{YENI_SCHEMA_ADI}' şeması kontrol ediliyor/oluşturuluyor...")
try:
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {YENI_SCHEMA_ADI}"))
        conn.commit()
    print(f"Şema '{YENI_SCHEMA_ADI}' başarıyla oluşturuldu/kontrol edildi.")
except Exception as e:
    print(f"Şema oluşturulurken HATA: {e}")
    # Hata durumunda devam etmeyebiliriz, belki de veritabanı kapalıdır.
    exit(1)


# Bu test satırı artık sorunu çözdüğümüzü doğrulayacak.
# Çıktıda modellerinizin tablo adlarını görmelisiniz (örn: 'users', 'products' vb.)
print("Base.metadata'ya KAYITLI TABLOLAR:", Base.metadata.tables.keys())

if not Base.metadata.tables:
    print("\n--- UYARI ---")
    print("Base.metadata'da hiçbir tablo bulunamadı.")
    print("backend.models.entities dosyasının modelleri 'Base'den miras aldığına emin olun.")
    print("-----------------\n")
else:
    print(f"'{YENI_SCHEMA_ADI}' şeması içine tablolar oluşturuluyor...")
    
    # create_all komutunu *burada* çalıştırıyoruz.
    Base.metadata.create_all(bind=engine)
    
    print("Tüm tablolar başarıyla oluşturuldu/kontrol edildi!")