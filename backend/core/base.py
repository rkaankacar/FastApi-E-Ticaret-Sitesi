from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


YENI_SCHEMA_ADI = "saat_satis"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:2004@localhost:5432/clockdatabase"

metadata_obj = MetaData(schema=YENI_SCHEMA_ADI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"options": f"-csearch_path={YENI_SCHEMA_ADI}"})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(metadata=metadata_obj)
