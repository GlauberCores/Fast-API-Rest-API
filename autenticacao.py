from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from dependencias import pegar_sessao
from models import Usuario
from schemas import UsuarioSchema, LoginSchema
from security import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM, oauth2_scheme

load_dotenv()

auth = APIRouter(prefix="/auth", tags=["auth"])

 #JWT (Json Web Token) -> Header, Payload, Signature
    #id_usuario -> Payload
   # data_expiracao -> Payload
def criar_token(id_usuario, tipo="access", duracao=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao
    dic_info = {
        "sub": str(id_usuario),
        "exp": data_expiracao,
        "type": tipo
    }
    return jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)

def verificar_refresh_token(token: str = Depends(oauth2_scheme), session: Session = Depends(pegar_sessao)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Token não é refresh")

        id_usuario = payload.get("sub")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = session.query(Usuario).filter(Usuario.id == int(id_usuario)).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return usuario

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    if not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario
@auth.get("/")
async def Home():
    """
    Essa é a rota padrão de login
    :return:
    """
    return {'mensagem':'você acessou a rota padrão de autenticação',"autenticação": False}

@auth.post("/Cadastrar") 
async def Cadastrar(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Email já está cadastrado")

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
async def Login(loginSchema: LoginSchema, session: Session=Depends(pegar_sessao)):
    usuario = autenticar_usuario(loginSchema.email, loginSchema.senha, session)

    if not usuario:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")
    else:
        access_token = criar_token(usuario.id, tipo="access")
        refresh_token = criar_token(usuario.id, tipo="refresh", duracao=timedelta(days=7))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }
@auth.get("/Refresh")
async def Refresh(usuario: Usuario = Depends(verificar_refresh_token)):
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
        
    }

@auth.post("/Login_form")
async def Login_from(dados_fomulario: OAuth2PasswordRequestForm = Depends(), session: Session=Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_fomulario.username, dados_fomulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
