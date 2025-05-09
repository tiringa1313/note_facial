from sqlalchemy import Column, String, Text, Date, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    face_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    nome = Column(Text, nullable=False)
    documento_identificacao = Column(Text, nullable=False)
    nome_mae = Column(Text)
    nome_pai = Column(Text)
    data_nascimento = Column(Date)
    naturalidade = Column(Text)
    sexo = Column(Text)
    cnh_numero = Column(Text)
    validade_cnh = Column(Date)
    categoria_cnh = Column(Text)
    telefones = Column(Text)
    endereco = Column(Text)
    alcunhas = Column(Text)
    profissao = Column(Text)
    foto_url = Column(Text)
    data_cadastro = Column(TIMESTAMP, server_default=func.now())
