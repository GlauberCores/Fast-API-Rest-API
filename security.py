from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import  OAuth2PasswordBearer

import os

load_dotenv()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Valores obrigatórios carregados do .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não configurada no .env")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/Login_form")
