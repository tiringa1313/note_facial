from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
import os

from app.routes import face_routes, cadastro_routes
from app.database import Base, engine
from app.models.pessoa_model import Pessoa

# ✅ Garante que as pastas necessárias existem
os.makedirs("base_faces", exist_ok=True)
os.makedirs("base_embeddings", exist_ok=True)

app = FastAPI()

# ✅ Rotas
app.include_router(face_routes.router)
app.include_router(cadastro_routes.router)

# ✅ Servir imagens recortadas de rostos
app.mount("/base_faces", StaticFiles(directory="base_faces"), name="base_faces")

# ✅ Criar tabelas automaticamente
Base.metadata.create_all(bind=engine)
