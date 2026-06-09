import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

PORT = int(os.getenv("PORT", 5000))
HOST = os.getenv("HOST", "0.0.0.0")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta-padrao-fallback-super-segura-123456")
DATABASE_PATH = os.getenv("DATABASE_PATH", "loja.db")
ENABLE_ADMIN_QUERY = os.getenv("ENABLE_ADMIN_QUERY", "False").lower() in ("true", "1", "yes")
