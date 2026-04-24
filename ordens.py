from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencias import pegar_sessao, verificar_token
from models import ItensPedido, Pedido, Usuario
from schemas import ItensPedidoSchema, ResponsePedidoSchema, PedidoSchema


orders = APIRouter(prefix="/orders", tags=["orders"])


def buscar_pedido(session: Session, id_pedido: int) -> Pedido:
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido nao encontrado")
    return pedido


def validar_acesso_pedido(usuario: Usuario, pedido: Pedido) -> None:
    if not usuario.admin and pedido.usuario != usuario.id:
        raise HTTPException(status_code=403, detail="Acesso negado")


def buscar_item(session: Session, id_item_pedido: int) -> ItensPedido:
    item = session.query(ItensPedido).filter(ItensPedido.id == id_item_pedido).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item do pedido nao encontrado")
    return item


@orders.get("/", response_model=list[ResponsePedidoSchema])
async def listar_pedidos(
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    """Lista os pedidos do usuario autenticado."""
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    return pedidos


@orders.get("/listar")
async def listar_pedidos_admin(
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """Lista todos os pedidos para administradores."""
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso negado")

    pedidos = session.query(Pedido).all()
    return [
        {"id": pedido.id, "usuario": pedido.usuario, "status": pedido.status, "preco": pedido.preco}
        for pedido in pedidos
    ]


@orders.get("/usuario/{id_usuario}", response_model=list[ResponsePedidoSchema])
async def listar_pedidos_por_usuario(
    id_usuario: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """Lista os pedidos de um usuario especifico; apenas admins podem usar."""
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso negado")

    pedidos = session.query(Pedido).filter(Pedido.usuario == id_usuario).all()
    return pedidos


@orders.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponsePedidoSchema)
async def criar_pedido(
    pedido_schema: PedidoSchema,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    """Cria um pedido para o usuario autenticado."""
    novo_pedido = Pedido(
        usuario=usuario.id,
        status=pedido_schema.status or "Pendente",
        preco=0.0,
    )
    session.add(novo_pedido)
    session.commit()
    session.refresh(novo_pedido)
    return novo_pedido


@orders.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(
    id_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """Cancela um pedido proprio ou qualquer pedido se o usuario for admin."""
    pedido = buscar_pedido(session, id_pedido)
    validar_acesso_pedido(usuario, pedido)

    pedido.status = "CANCELADO"
    session.commit()
    session.refresh(pedido)

    return {
        "msg": f"Pedido numero {id_pedido} cancelado com sucesso",
        "pedido": {"id": pedido.id, "status": pedido.status, "preco": pedido.preco},
    }


@orders.post("/pedido/{id_pedido}/items", status_code=status.HTTP_201_CREATED)
async def adicionar_item(
    id_pedido: int,
    item_schema: ItensPedidoSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """Adiciona um item a um pedido permitido para o usuario."""
    pedido = buscar_pedido(session, id_pedido)
    validar_acesso_pedido(usuario, pedido)

    item = ItensPedido(
        quantidade=item_schema.quantidade,
        sabor=item_schema.sabor,
        preco_unitario=item_schema.preco_unitario,
        pedido=pedido.id,
    )
    session.add(item)
    session.flush()

    pedido.calcular_preco()
    session.commit()
    session.refresh(item)
    session.refresh(pedido)

    return {
        "msg": f"Item adicionado ao pedido numero {id_pedido} com sucesso",
        "item": {
            "id": item.id,
            "quantidade": item.quantidade,
            "sabor": item.sabor,
            "preco_unitario": item.preco_unitario,
        },
        "preco_total": pedido.preco,
    }


@orders.delete("/pedido/item/{id_item_pedido}")
async def remover_item(
    id_item_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """Remove um item do pedido e recalcula o valor total."""
    item = buscar_item(session, id_item_pedido)
    pedido = buscar_pedido(session, item.pedido)
    validar_acesso_pedido(usuario, pedido)

    session.delete(item)
    session.flush()

    pedido.calcular_preco()
    session.commit()
    session.refresh(pedido)

    return {
        "msg": f"Item removido do pedido numero {pedido.id} com sucesso",
        "pedido": {"id": pedido.id, "status": pedido.status, "preco": pedido.preco},
    }
