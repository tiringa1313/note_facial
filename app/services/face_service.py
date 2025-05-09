import uuid

import cv2
import numpy as np
from fastapi import UploadFile
from app.services.embedding_service import gerar_embedding
from app.services.comparador_service import comparar_com_base
from app.services.registro_service import registrar_novo_rosto


# Carrega o classificador HaarCascade
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

async def verificar_rosto(file: UploadFile):
    try:
        # Lê o conteúdo do arquivo
        contents = await file.read()
        npimg = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if image is None:
            return {"erro": "Não foi possível ler a imagem."}

        # Detecta rosto (validação básica)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            return {"rosto_detectado": False}

        # Gera o embedding facial
        embedding = gerar_embedding(image)

        if embedding is None:
            return {"erro": "Não foi possível gerar o vetor facial."}

        # Compara com a base de embeddings
        id_encontrado = comparar_com_base(embedding)

        if id_encontrado:
            return {
                "rosto_detectado": True,
                "ja_cadastrado": True,
                "id": id_encontrado,
                "mensagem": "Rosto já cadastrado na base"
            }

        # Caso novo: apenas retorna ID temporário + vetor (sem salvar)
        id_temporario = str(uuid.uuid4())

        return {
            "rosto_detectado": True,
            "ja_cadastrado": False,
            "face_id_temporario": id_temporario,
            "embedding": embedding.tolist(),  # opcional
            "mensagem": "Rosto detectado, pronto para cadastro"
        }


    except Exception as e:
        return {"erro": str(e)}
