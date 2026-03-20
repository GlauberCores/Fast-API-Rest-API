from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencias import pegar_sessao, verificar_token
from models import Pedido, Usuario, ItensPedido
from schemas import PedidoSchema, ItensPedidoSchema

# Dependencia de autenticacao aplicada a todas as rotas deste router
orders = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verificar_token)])


@orders.get("/")
async def listar_pedidos(
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    """Lista os pedidos do usuario autenticado."""
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    return [{"id": p.id, "status": p.status, "preco": p.preco} for p in pedidos]


@orders.get("/listar")
async def listar_pedidos_admin(
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """Lista todos os pedidos (apenas admins)."""
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Acesso negado")
    pedidos = session.query(Pedido).all()
    return [{"id": p.id, "usuario": p.usuario, "status": p.status, "preco": p.preco} for p in pedidos]


@orders.post("/", status_code=201)
async def criar_pedido(
    pedido_schema: PedidoSchema,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao),
):
    """Cria um pedido para o usuario autenticado."""
    novo_pedido = Pedido(
        usuario=usuario.id,
        status=pedido_schema.status or "Pendente",
        preco=pedido_schema.preco or 0.0,
    )
    session.add(novo_pedido)
    session.commit()
    session.refresh(novo_pedido)
    return {"id": novo_pedido.id, "status": novo_pedido.status, "preco": novo_pedido.preco}


@orders.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(
    id_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """Cancela um pedido. Admins podem cancelar qualquer pedido; usuarios comuns apenas os proprios."""
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
    if not usuario.admin and pedido.usuario != usuario.id:
        raise HTTPException(status_code=401, detail="Acesso negado")
    pedido.status = "CANCELADO"
    session.commit()
    return {"msg": f"Pedido numero {id_pedido} cancelado com sucesso", "pedido": pedido}


@orders.post("/pedido/{id_pedido}/items", status_code=201)
async def adicionar_item(
    id_pedido: int,
    item_schema: ItensPedidoSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """Adiciona item a um pedido do usuario (ou qualquer pedido se admin)."""
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")
    if not usuario.admin and pedido.usuario != usuario.id:
        raise HTTPException(status_code=401, detail="Acesso negado")

    item = ItensPedido(
        quantidade=item_schema.quantidade,
        sabor=item_schema.sabor,
        preco_unitario=item_schema.preco_unitario,
        pedido=id_pedido,
    )
    session.add(item)
    session.commit()
    session.refresh(item)

    # atualiza o preco total do pedido apos inserir o item
    pedido.calcular_preco()
    session.commit()

    return {
        "msg": f"Item adicionado ao pedido numero {id_pedido} com sucesso",
        "item": {"id": item.id, "quantidade": item.quantidade, "preco_unitario": item.preco_unitario},
        "preco_total": pedido.preco,
    }
