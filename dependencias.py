from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from fastapi import Depends, HTTPException

from models import db, Usuario
from security import SECRET_KEY, ALGORITHM, oauth2_scheme

# Sessão única por requisição
SessionLocal = sessionmaker(bind=db, autoflush=False, autocommit=False)


def pegar_sessao():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def verificar_token(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(pegar_sessao)
):
    """
    Valida o JWT de acesso e retorna o usuário autenticado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = payload.get("sub")
        if id_usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = session.query(Usuario).filter(Usuario.id == int(id_usuario)).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso negado")

    return usuario
