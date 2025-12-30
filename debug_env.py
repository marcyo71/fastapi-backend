import os
from app.config.settings import load_settings

print("=== DEBUG ENVIRONMENT ===")
print("ENV variable:", os.getenv("ENV", "dev"))

# stampa tutte le variabili d'ambiente attive
print("\n--- SYSTEM ENV ---")
for k, v in os.environ.items():
    if "DATABASE" in k or "ASYNC" in k or "ENV" in k:
        print(f"{k}={v}")

# carica le settings
print("\n--- SETTINGS ---")
settings = load_settings()
print(settings.model_dump())
import os
from app.config.settings import load_settings

print("=== DEBUG ENVIRONMENT ===")
print("ENV variable:", os.getenv("ENV", "dev"))

# stampa tutte le variabili d'ambiente attive
print("\n--- SYSTEM ENV ---")
for k, v in os.environ.items():
    if "DATABASE" in k or "ASYNC" in k or "ENV" in k:
        print(f"{k}={v}")

# carica le settings
print("\n--- SETTINGS ---")
settings = load_settings()
print(settings.model_dump())
