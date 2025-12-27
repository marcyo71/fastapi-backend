# Usa un'immagine base più leggera
FROM python:3.11-slim

# Imposta la working directory
WORKDIR /app

# Evita output bufferizzato
ENV PYTHONUNBUFFERED=1

# Installa dipendenze di sistema (per psycopg2 e compilazioni)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia solo requirements per sfruttare la cache
COPY requirements.txt .

# Installa le dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice
COPY . .

# Espone la porta
EXPOSE 8000

# Comando di avvio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
