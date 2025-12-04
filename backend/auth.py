import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from backend.config.settings import settings

# -------------------
# CONFIGURAZIONE JWT
# -------------------
# Usa settings, con fallback alle variabili d'ambiente per sicurezza
SECRET_KEY = settings.secret_key or os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = settings.algorithm or os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = (
    settings.access_token_expire_minutes
    or int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
)

# -------------------
# CREA TOKEN
# -------------------
def create_access_token(data: dict) -> str:
    """
    Crea un JWT con payload personalizzato e scadenza.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# -------------------
# VERIFICA TOKEN
# -------------------
def verify_token(token: str) -> dict | None:
    """
    Verifica e decodifica un JWT. Restituisce il payload se valido, altrimenti None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Token decodificato:", payload)  # DEBUG
        return payload
    except JWTError as e:
        print("Errore verify_token:", e)  # DEBUG
        return None
