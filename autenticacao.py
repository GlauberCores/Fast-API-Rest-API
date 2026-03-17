from fastapi import APIRouter,Depends,HTTPException
from dependencias import pegar_sessao
from sqlalchemy.orm import Session
from models import Usuario
from security import bcrypt_context
from schemas import *

auth = APIRouter(prefix="/auth", tags=["auth"])

@auth.get("/")
async def Home():
    """
    Essa é a rota padrão de login
    :return:
    """
    return {'mensagem':'você acessou a rota padrão de autenticação',"autenticação": False}

@auth.post("/Cadastrar") 
async def Cadastrar(usuario_schema: UsuarioSchema, session=Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(
        nome=usuario_schema.nome,
        email=usuario_schema.email,
        senha=senha_criptografada,
        ativo=usuario_schema.ativo if usuario_schema.ativo is not None else True,
        admin=usuario_schema.admin if usuario_schema.admin is not None else False
    )

        session.add(novo_usuario)
        session.commit()

        return {"msg": f"usuario cadastrado com sucesso {usuario_schema.email}"}


#login -> email e senha -> JWT (Json Web Token)
@auth.post("/Login")
async def Login(loginSchema: LoginSchema, session=Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == loginSchema.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")
    
    if not bcrypt_context.verify(loginSchema.senha, usuario.senha):
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")
    
    return {"msg": f"Login bem-sucedido para {loginSchema.email}"}