from sqlalchemy import create_engine,Column,Integer,String,Boolean,Float,ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType

#cria conexão com seu banco
db= create_engine("sqlite:///database.db")

#cria a base do banco de dados
Base= declarative_base()

#cria as classes/tabelas do banco
class Usuario(Base):
 # Usuario
    __tablename__ = 'usuarios'

    id    = Column('id', Integer, primary_key=True, autoincrement=True)#
    nome  = Column('nome', String)
    email = Column('email', String,nullable=False)
    senha = Column('senha', String)
    ativo = Column('ativo', Boolean)
    admim = Column('admim', Boolean,default=False)

    def __init__(self, nome, email, senha, ativo=True, admim=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admim = admim
#Pedidos
class Pedido(Base):
    __tablename__ = 'pedidos'

   # STATUS_PEDIDOS = (
   #     ('PENDENTE','PENDENTE'),
   #     ('CANCELADO','CANCELADO'),
   #     ('FINALIZADO','FINALIZADO')
   # )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    status = Column('status', String)# Pendente, Cancelado,
    usuario= Column('usuario', ForeignKey('usuarios.id'))
    preco = Column('preco', Float)


    def __init__(self,usuario,status='Pendente',preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco
    #itens =

#ItensPedido
class ItensPedido(Base):
    __tablename__ = 'itens_pedido'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    quantidade = Column('quantidade', Integer)
    sabor = Column('sabor', String)
    preco_unitario = Column('preco', Float)
    pedido = Column('pedido', ForeignKey('pedidos.id'))

def __init__(self,quantidade,sabor,preco_unitario,pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.preco_unitario = preco_unitario
        self.pedido = pedido

#executa a criação dos metadados do seu banco(cria o banco de dados)
# alembic revision --autogenerate -m "Migracao Inicial"

#atulizar banco
#alambic upgrade head kd