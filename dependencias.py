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

def verificar_token(token: str, session: Session=Depends(pegar_sessao)):   
    usuario = session.query(Usuario).filter(Usuario.id == 1).first()
    return usuario