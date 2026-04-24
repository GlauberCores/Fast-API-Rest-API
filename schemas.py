from pydantic import BaseModel
from typing import Optional


class UsuarioSchema(BaseModel):# UsuarioSchema é um modelo de dados que representa as informações de um usuário.
                               # Ele é usado para validar e serializar os dados de entrada e saída relacionados aos usuários em uma aplicação.
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
      from_attributes = True # Permite a conversão de atributos do modelo 
                             # para os campos do schema,
                             #   facilitando a integração entre os modelos de dados e os esquemas de validaçã

class PedidoSchema(BaseModel):
    status: Optional[str] = "Pendente"
    preco: Optional[float] = 0.0

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

class ItensPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    preco_unitario: float
    pedido: Optional[int] = None

    class Config:
        from_attributes = True


class ResponsePedidoSchema(BaseModel):
    id: int
    status: str
    preco: float

    class Config:
        from_attributes = True


# Compatibilidade com o nome antigo usado no projeto.
ResnponsePedidoSchema = ResponsePedidoSchema
