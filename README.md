## Funcionalidades
- Cadastro de usuários
- Autenticação com JWT (access/refresh)
- Criação de pedidos
- Estrutura modular com rotas separadas

## Como rodar o projeto
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
```

## Preview da API
Abra http://127.0.0.1:8000/docs para testar as rotas interativamente.
