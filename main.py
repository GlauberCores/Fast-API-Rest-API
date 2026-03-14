from fastapi import FastAPI
from autenticacao import auth
from ordens import orders
#para roda nosso codigo no terminal  uvicorn main:app --reload
app = FastAPI()

#endpoint:
#/ordens(patch)caminho

#Rest APIs
#Get -> leitura/pegar
#Post -> enviar/criar
#Put/Patch -> edição
#Delete -> deletar
app.include_router(auth)
app.include_router(orders)
@app.get("/")