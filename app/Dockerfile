# Usa immagine Python ufficiale
FROM python:3.11-slim

# Imposta la working directory
WORKDIR /app

# Copia requirements e installa dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice
COPY . .

# Espone la porta
EXPOSE 8000

# Avvia FastAPI con Uvicorn
CMD ["uvicorn", "fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
