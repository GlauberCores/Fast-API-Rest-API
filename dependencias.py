from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

def pegar_sessao():
    try:   
        Session = sessionmaker(bind = db)
        session = Session()
        yield session           #yield é usado para criar um gerador, que é uma função que pode ser pausada e retomada, permitindo que o código seja executado de forma assíncrona e eficiente.
    finally:
        session.close()