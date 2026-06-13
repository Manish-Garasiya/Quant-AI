from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:Mannu%2307@localhost:5432/quant_ai"

db_engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=db_engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_session():
    return SessionLocal()

