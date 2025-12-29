FROM python:3.11-slim

# Evita output bufferizzato
ENV PYTHONUNBUFFERED=1

# Installa dipendenze di sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea directory app
WORKDIR /app

# Copia requirements
COPY requirements.txt .

# Installa dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il progetto
COPY . .

# Espone la porta FastAPI
EXPOSE 8000

# Usa l'entrypoint (lo creiamo dopo)
ENTRYPOINT ["/app/docker-entrypoint.sh"]
