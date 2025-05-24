FROM python:3.10-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho no container
WORKDIR /app

# Copia os arquivos para o container
COPY . /app

# Atualiza o pip para a versão mais recente
RUN python -m pip install --upgrade pip

# Instala as dependências do projeto
RUN pip install -r requirements.txt

# Expõe a porta padrão do FastAPI
EXPOSE 10000

# Comando para iniciar a API
EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

