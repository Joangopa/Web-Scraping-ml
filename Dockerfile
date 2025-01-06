# Usa uma imagem do Python
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo requirements.txt para o container
COPY requirements.txt .

# Instala as dependências do projeto        
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto para o container
COPY . .

# Expoe a porta do Postgres
EXPOSE 5432

# rodar o aplicativo
CMD ["python", "app_postgres.py"]
