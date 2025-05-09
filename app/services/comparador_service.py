import os
import numpy as np
from scipy.spatial.distance import cosine

PASTA_EMBEDDINGS = "dados_faces"
LIMIAR_SIMILARIDADE = 0.5  # Ajustável (menor = mais rigoroso)

def comparar_com_base(embedding_np):
    """
    Compara o vetor facial recebido com todos os embeddings salvos.
    Retorna o nome do arquivo correspondente se houver correspondência.
    """
    if not os.path.exists(PASTA_EMBEDDINGS):
        os.makedirs(PASTA_EMBEDDINGS)

    for nome_arquivo in os.listdir(PASTA_EMBEDDINGS):
        if nome_arquivo.endswith(".npy"):
            caminho = os.path.join(PASTA_EMBEDDINGS, nome_arquivo)
            emb_salvo = np.load(caminho)
            distancia = cosine(embedding_np, emb_salvo)

            if distancia < LIMIAR_SIMILARIDADE:
                id_pessoa = nome_arquivo.replace(".npy", "")
                return id_pessoa  # encontrou alguém

    return None  # não encontrou ninguém
