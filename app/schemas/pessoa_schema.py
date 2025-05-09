from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import date

class PessoaCreate(BaseModel):
    face_id: str
    nome: str
    documento_identificacao: str
    nome_mae: Optional[str]
    nome_pai: Optional[str]
    data_nascimento: Optional[date]
    naturalidade: Optional[str]
    sexo: Optional[str]
    cnh_numero: Optional[str]
    validade_cnh: Optional[date]
    categoria_cnh: Optional[str]
    telefones: Optional[str]
    endereco: Optional[str]
    alcunhas: Optional[str]
    profissao: Optional[str]

    embedding: List[float]

