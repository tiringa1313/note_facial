import os
from fastapi import APIRouter, UploadFile, File
from app.services.face_service import verificar_rosto

router = APIRouter(prefix="/face", tags=["Face"])


@router.post("/verificar")
async def verificar_face(file: UploadFile = File(...)):
    """
    Recebe uma imagem via upload e verifica se o rosto já está cadastrado.
    """
    resultado = await verificar_rosto(file)
    return resultado


@router.get("/cadastradas")
def listar_faces():
    """
    Lista todos os vetores faciais (.npy) salvos no servidor.
    """
    pasta = "base_embeddings"  # ✅ Atualizado para refletir o novo diretório
    if not os.path.exists(pasta):
        return {"arquivos": [], "mensagem": "Nenhum vetor encontrado."}

    arquivos = [f for f in os.listdir(pasta) if f.endswith(".npy")]
    return {"quantidade": len(arquivos), "arquivos": arquivos}
