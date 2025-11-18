import logging

logging.basicConfig(
    filename="logs/backend.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("backend")
from backend.config.settings import settings

print(settings.API_HOST)      # → "127.0.0.1"
print(settings.API_PORT)      # → 8000
print(settings.DEBUG)         # → "true"
print(settings.is_debug)      # → True (booleano)
print(settings.ENV)           # → "development"
import os
import logging

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  # ✅ crea la cartella se non esiste

logging.basicConfig(
    filename=os.path.join(log_dir, "backend.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

