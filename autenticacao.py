from fastapi import APIRouter,Depends,HTTPException
from dependencias import pegar_sessao,verificar_token
from sqlalchemy.orm import Session
from models import Usuario
from security import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from schemas import UsuarioSchema, LoginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()

auth = APIRouter(prefix="/auth", tags=["auth"])

 #JWT (Json Web Token) -> Header, Payload, Signature
    #id_usuario -> Payload
   # data_expiracao -> Payload
def criar_token(id_usuario,duracao = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao
    dic_info={"sub": id_usuario, "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado



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
    if len(usuario_schema.senha) > 72:
        raise HTTPException(
            status_code=400,
            detail="A senha deve ter no máximo 72 caracteres"
        )

    
    else:
        senha = usuario_schema.senha[:72]
        senha_criptografada = bcrypt_context.hash(senha)
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
    usuario = verificar_token(loginSchema.email, loginSchema.senha, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")

    acess_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao=timedelta(days=7))
    return {
        "acess_token": acess_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }
@auth.get("/Refresh")
async def Refresh(usuario: Usuario = Depends(verificar_token)):
    acess_token = criar_token(usuario.id)
    return {
        "acess_token": acess_token,
        "token_type": "Bearer"
    }