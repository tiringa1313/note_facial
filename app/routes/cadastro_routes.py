import os
import numpy as np
import cv2
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from scipy.spatial.distance import cosine

from app.models.pessoa_model import Pessoa
from app.database import SessionLocal

from app.services.registro_service import registrar_novo_rosto

router = APIRouter(prefix="/face", tags=["Face"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cadastrar")
async def cadastrar_pessoa(
    face_id: str = Form(...),
    nome: str = Form(...),
    documento_identificacao: str = Form(...),
    foto: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Verifica se já existe
    existente = db.query(Pessoa).filter(Pessoa.face_id == face_id).first()
    if existente:
        raise HTTPException(status_code=400, detail="Pessoa já cadastrada com este face_id.")

    # Ler imagem recebida
    conteudo = await foto.read()
    imagem_np = np.frombuffer(conteudo, np.uint8)
    imagem = cv2.imdecode(imagem_np, cv2.IMREAD_COLOR)

    # Gerar embedding com InsightFace
    embedding, face = gerar_embedding_insightface(imagem)
    if embedding is None:
        raise HTTPException(status_code=400, detail="Nenhum rosto detectado.")

    # Salvar vetor e imagem recortada
    registrar_novo_rosto(imagem, embedding, face)

    # Salvar imagem original (opcional)
    os.makedirs("base_faces", exist_ok=True)
    extensao = foto.filename.split(".")[-1]
    nome_arquivo = f"{face_id}.{extensao}"
    caminho_local = os.path.join("base_faces", nome_arquivo)
    with open(caminho_local, "wb") as f:
        f.write(conteudo)

    # URL pública Railway
    url_publica = f"https://notefacial-production.up.railway.app/base_faces/{nome_arquivo}"

    # Salvar no banco
    nova_pessoa = Pessoa(
        face_id=face_id,
        nome=nome,
        documento_identificacao=documento_identificacao,
        foto_url=url_publica
    )
    db.add(nova_pessoa)
    db.commit()
    db.refresh(nova_pessoa)

    return {
        "mensagem": "Pessoa cadastrada com sucesso!",
        "id": str(nova_pessoa.id),
        "foto_url": url_publica
    }


@router.get("/{face_id}")
def buscar_por_face_id(face_id: str, db: Session = Depends(get_db)):
    pessoa = db.query(Pessoa).filter(Pessoa.face_id == face_id).first()
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada.")

    return {
        "faceId": str(pessoa.face_id),
        "nome": pessoa.nome,
        "documentoIdentificacao": pessoa.documento_identificacao,
        "nomeMae": pessoa.nome_mae,
        "nomePai": pessoa.nome_pai,
        "dataNascimento": pessoa.data_nascimento.isoformat() if pessoa.data_nascimento else None,
        "naturalidade": pessoa.naturalidade,
        "sexo": pessoa.sexo,
        "cnhNumero": pessoa.cnh_numero,
        "validadeCnh": pessoa.validade_cnh.isoformat() if pessoa.validade_cnh else None,
        "categoriaCnh": pessoa.categoria_cnh,
        "telefones": pessoa.telefones,
        "endereco": pessoa.endereco,
        "alcunhas": pessoa.alcunhas,
        "profissao": pessoa.profissao,
        "fotoUrl": pessoa.foto_url,
    }


@router.post("/buscar_por_imagem")
async def buscar_por_imagem(
    foto: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    conteudo = await foto.read()
    imagem_np = np.frombuffer(conteudo, np.uint8)
    imagem = cv2.imdecode(imagem_np, cv2.IMREAD_COLOR)

    # Gerar embedding com InsightFace
    embedding_novo, _ = gerar_embedding_insightface(imagem)
    if embedding_novo is None:
        raise HTTPException(status_code=400, detail="Nenhum rosto detectado.")

    # Comparar com embeddings existentes
    pasta = "base_embeddings"
    limiar = 0.35  # cosine similarity ideal para ArcFace

    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith(".npy"):
            caminho = os.path.join(pasta, nome_arquivo)
            embedding_existente = np.load(caminho)

            distancia = cosine(embedding_existente, embedding_novo)
            if distancia < limiar:
                face_id = nome_arquivo.replace(".npy", "")
                pessoa = db.query(Pessoa).filter(Pessoa.face_id == face_id).first()
                if pessoa:
                    return {
                        "encontrado": True,
                        "faceId": str(pessoa.face_id),
                        "nome": pessoa.nome,
                        "documentoIdentificacao": pessoa.documento_identificacao,
                        "fotoUrl": pessoa.foto_url,
                        # outros campos se desejar
                    }

    return {"encontrado": False}
