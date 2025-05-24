import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Dados de conexão
DATABASE_URL = os.getenv("DATABASE_URL")


# Criar engine
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()


# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()
