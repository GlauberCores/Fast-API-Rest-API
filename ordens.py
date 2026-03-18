from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencias import pegar_sessao, verificar_token
from models import Pedido, Usuario
from schemas import PedidoSchema

orders = APIRouter(prefix="/orders", tags=["orders"])


@orders.get("/")
async def listar_pedidos(
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)
):
    """
    Lista os pedidos do usuário autenticado.
    """
    pedidos = (
        session.query(Pedido)
        .filter(Pedido.usuario == usuario.id)
        .all()
    )
    return [
        {"id": p.id, "status": p.status, "preco": p.preco}
        for p in pedidos
    ]


@orders.post("/", status_code=201)
async def criar_pedido(
    pedido_schema: PedidoSchema,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)
):
    """
    Cria um pedido para o usuário autenticado.
    """
    novo_pedido = Pedido(
        usuario=usuario.id,
        status=pedido_schema.status or "Pendente",
        preco=pedido_schema.preco or 0.0,
    )
    session.add(novo_pedido)
    session.commit()
    session.refresh(novo_pedido)

    return {
        "id": novo_pedido.id,
        "status": novo_pedido.status,
        "preco": novo_pedido.preco,
    }
