from insightface.app import FaceAnalysis
import numpy as np

# Carrega o modelo ArcFace com CPU (ideal para servidores)
app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0)

def gerar_embedding_insightface(image_np):
    """
    Gera o embedding facial com ArcFace (InsightFace).
    Retorna: (vetor_embedding, objeto_face) ou (None, None) se falhar.
    """
    faces = app.get(image_np)
    if not faces:
        return None, None

    face = faces[0]
    embedding = face.embedding / np.linalg.norm(face.embedding)  # normalização é crucial
    return embedding, face
