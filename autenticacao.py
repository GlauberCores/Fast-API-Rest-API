from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from models import *

auth = APIRouter(prefix="/auth", tags=["auth"])

@auth.get("/")
async def Home():
    """
    Essa é a rota padrão de login
    :return:
    """
    return {'mensagem':'você acessou a rota padrão de autenticação'}
@auth.post("/login")
async def Login(email=str, senha=str,nome=str):
        Session = sessionmaker(bind=db)
        session = Session()
        usuario = session.query(Usuario).filter(Usuario.email == email).first()
        if usuario:
            # ja existe um usuario com o esse email

            return {"msg": "já existe um usuário cadastrado com esse email"}
        else:
            novo_usuario = Usuario(email=email, senha=senha)
            session.add(novo_usuario)
            session.commit()
            return {"msg": "usuario cadastrado com sucesso"}
        async