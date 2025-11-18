from passlib.context import CryptContext

# Configura il contesto di hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Restituisce l'hash della password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se la password in chiaro corrisponde all'hash"""
    return pwd_context.verify(plain_password, hashed_password)
