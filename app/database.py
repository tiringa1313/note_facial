import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ Captura e limpa a URL do banco
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

# ✅ Cria o engine (AGORA SIM, definido antes de usar)
engine = create_engine(DATABASE_URL)

# ✅ Cria a sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base para os modelos
Base = declarative_base()
