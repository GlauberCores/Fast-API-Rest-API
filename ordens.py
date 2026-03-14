from fastapi import APIRouter

orders = APIRouter(prefix='/orders', tags=["orders"])

@orders.get("/ordens")
async def pedidos():
    """
    essa é a rota padrão de pedidos
    :return:
    """
    return {"msg":'você acessou a rota de pedidos'}