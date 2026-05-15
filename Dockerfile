# Imagem base leve com Python 3.11
FROM python:3.11-slim

# Evita geração de .pyc e garante logs sem buffer no container
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copia e instala dependências primeiro (camada cacheável pelo Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Porta exposta pela aplicação
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
