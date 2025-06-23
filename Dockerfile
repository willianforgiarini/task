FROM python:3.11-slim

# Define a variável de ambiente para garantir que a saída dos logs seja exibida imediatamente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependências para o container
COPY requirements.txt .

# Instala as dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante da aplicação para dentro do container
COPY . .

# Comonado padrão do container: inicia o servidor Gunicorn
CMD gunicorn conf.wsgi:application --bind 0.0.0.0:8000