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
    usuario: int
   
    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True