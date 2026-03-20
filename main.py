from fastapi import FastAPI
from dotenv import load_dotenv

from autenticacao import auth
from ordens import orders

load_dotenv()
app = FastAPI()

# para rodar no terminal: uvicorn main:app --reload
app.include_router(auth)
app.include_router(orders)


@app.get("/")
async def home():
    """Rota padrao de home."""
    return {"mensagem": "voce acessou a rota padrao de home"}
