from fastapi import APIRouter, Depends
from dependencias import pegar_sessao
from sqlalchemy.orm import Session
from schemas import PedidoSchema
from models import Pedido
orders = APIRouter(prefix='/orders', tags=["orders"])

@orders.get("/ordens")
async def pedidos():
    """
    essa é a rota padrão de pedidos
    :return:
    """
    return {"msg":'você acessou a rota de pedidos'}
@orders.post("/Pedido")
async def criar_pedido(pedidoschema:PedidoSchema,session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedidoschema.usuario)
    session.add(novo_pedido)
    session.commit()

    """
    essa é a rota de criação de pedidos
    :return:
    """
    return {"msg":'você acessou a rota de criação de pedidos'}