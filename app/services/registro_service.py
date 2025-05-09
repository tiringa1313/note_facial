import cv2
import numpy as np
import uuid
import os

PASTA_EMBEDDINGS = "base_embeddings"
PASTA_IMAGENS = "base_faces"

def registrar_novo_rosto(image_np, embedding, face):
    """
    Salva a imagem recortada do rosto + vetor facial.
    Retorna o ID único gerado para posterior associação com os dados da pessoa.
    """
    id_rosto = str(uuid.uuid4())

    # Extrai as coordenadas do bounding box do objeto 'face' do InsightFace
    x1, y1, x2, y2 = face.bbox.astype(int)
    rosto_recortado = image_np[y1:y2, x1:x2]

    # Salva imagem
    caminho_img = os.path.join(PASTA_IMAGENS, f"{id_rosto}.jpg")
    cv2.imwrite(caminho_img, rosto_recortado)

    # Salva embedding (já deve estar normalizado)
    caminho_emb = os.path.join(PASTA_EMBEDDINGS, f"{id_rosto}.npy")
    np.save(caminho_emb, embedding)

    return id_rosto
