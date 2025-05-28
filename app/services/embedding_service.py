from insightface.app import FaceAnalysis
import numpy as np

_face_app = None

def get_face_app():
    global _face_app
    if _face_app is None:
        _face_app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
        _face_app.prepare(ctx_id=0)
    return _face_app

def gerar_embedding_insightface(image_np):
    app = get_face_app()
    faces = app.get(image_np)
    if not faces:
        return None, None

    face = faces[0]
    embedding = face.embedding / np.linalg.norm(face.embedding)
    return embedding, face
