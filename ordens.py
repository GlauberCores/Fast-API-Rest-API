from fastapi import APIRouter, Depends
from dependencias import pegar_sessao
from sqlalchemy.orm import Session
from schemas import PedidoSchema
orders = APIRouter(prefix='/orders', tags=["orders"])

@orders.get("/ordens")
async def pedidos():
    """
    essa é a rota padrão de pedidos
    :return:
    """
    return {"msg":'você acessou a rota de pedidos'}
@orders.post("/Pedido")
async def criar_pedido(pedifoschema:PedidoSchema,session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=PedidoSchema.id_usuario)
    """
    essa é a rota de criação de pedidos
    :return:
    """
    return {"msg":'você acessou a rota de criação de pedidos'}