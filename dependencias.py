from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import *
from dotenv import load_dotenv
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
import os


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def pegar_sessao():
    try:   
        Session = sessionmaker(bind = db)
        session = Session()
        yield session           #yield é usado para criar um gerador, que é uma função que pode ser pausada e retomada, permitindo que o código seja executado de forma assíncrona e eficiente.
    finally:
        session.close()

def verificar_token(token, session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = dic_info.get("sub")

        if not id_usuario:
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso negado")

    return usuario