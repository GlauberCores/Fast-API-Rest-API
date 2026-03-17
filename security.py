from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import  OAuth2PasswordBearer
import os

load_dotenv()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
OAuth2PasswordBearer= OAuth2PasswordBearer(tokenUrl="/auth/Login")