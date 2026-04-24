# Fast API Rest API

API REST desenvolvida com FastAPI para cadastro de usuarios, autenticacao com JWT e gerenciamento de pedidos com itens. O projeto usa SQLite como banco local, SQLAlchemy como ORM e Pydantic para validacao de entrada e saida.

## Objetivo do projeto

Este projeto implementa uma base de API para:

- registrar usuarios com senha criptografada;
- autenticar usuarios com `access_token` e `refresh_token`;
- criar pedidos vinculados ao usuario autenticado;
- adicionar e remover itens de um pedido;
- recalcular o valor total do pedido automaticamente;
- permitir operacoes administrativas sobre pedidos.

## Stack utilizada

- Python 3.13
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Passlib com bcrypt
- python-jose para JWT
- python-multipart para `OAuth2PasswordRequestForm`
- SQLite
- Pytest / HTTPX para testes

## Estrutura do projeto

```text
.
|-- alembic/
|-- autenticacao.py
|-- dependencias.py
|-- main.py
|-- models.py
|-- ordens.py
|-- schemas.py
|-- security.py
|-- requirements.txt
|-- .env
`-- database.db
```

## Arquitetura dos modulos

- `main.py`
  Ponto de entrada da aplicacao. Registra os routers de autenticacao e pedidos.
- `autenticacao.py`
  Contem cadastro de usuario, login JSON, login via formulario OAuth2 e refresh token.
- `ordens.py`
  Implementa as rotas de pedidos e itens, incluindo validacao de acesso por usuario/admin.
- `dependencias.py`
  Cria a sessao SQLAlchemy por requisicao e valida o token JWT de acesso.
- `models.py`
  Define as tabelas `usuarios`, `pedidos` e `itens_pedido`.
- `schemas.py`
  Define os contratos de entrada e resposta via Pydantic.
- `security.py`
  Centraliza hash de senha, configuracao JWT e `OAuth2PasswordBearer`.

## Modelo de dados

### Usuario

- `id`: identificador do usuario
- `nome`: nome do usuario
- `email`: unico
- `senha`: hash bcrypt
- `ativo`: flag de status
- `admin`: flag de permissao administrativa

### Pedido

- `id`: identificador do pedido
- `status`: estado atual do pedido
- `usuario`: chave estrangeira para `usuarios.id`
- `preco`: valor total do pedido

### ItensPedido

- `id`: identificador do item
- `quantidade`: quantidade do item
- `sabor`: descricao do item
- `preco_unitario`: valor unitario
- `pedido`: chave estrangeira para `pedidos.id`

O valor total do pedido e recalculado pelo metodo `Pedido.calcular_preco()` a partir dos itens relacionados.

## Variaveis de ambiente

O arquivo `.env` esperado pelo projeto:

```env
SECRET_KEY=seu_token_secreto
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Instalacao e execucao

### 1. Clonar o repositorio

```bash
git clone https://github.com/GlauberCores/Fast-API-Rest-API.git
cd Fast-API-Rest-API
```

### 2. Criar e ativar ambiente virtual

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Subir a API

```bash
uvicorn main:app --reload
```

Aplicacao disponivel em:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Fluxo de autenticacao

### Cadastro de usuario

`POST /auth/Cadastrar`

Recebe `nome`, `email`, `senha`, `ativo` e `admin`.

### Login com JSON

`POST /auth/Login`

Recebe `email` e `senha`, e retorna:

```json
{
  "access_token": "jwt",
  "refresh_token": "jwt",
  "token_type": "Bearer"
}
```

### Refresh de token

`GET /auth/Refresh`

Requer um `refresh_token` no header `Authorization`.

### Login de formulario OAuth2

`POST /auth/Login_form`

Usado para integracao com o fluxo padrao do Swagger e do `OAuth2PasswordBearer`.

## Rotas principais

### Rotas gerais

- `GET /`
  Health endpoint basico da aplicacao.

### Autenticacao

- `GET /auth/`
  Rota informativa do modulo de autenticacao.
- `POST /auth/Cadastrar`
  Cria usuario novo.
- `POST /auth/Login`
  Autentica por JSON.
- `POST /auth/Login_form`
  Autentica por formulario.
- `GET /auth/Refresh`
  Gera novo `access_token` a partir de um refresh valido.

### Pedidos

Todas as rotas abaixo exigem token Bearer valido.

- `GET /orders/`
  Lista os pedidos do usuario autenticado.
- `GET /orders/listar`
  Lista todos os pedidos. Somente admin.
- `GET /orders/usuario/{id_usuario}`
  Lista pedidos de um usuario especifico. Somente admin.
- `POST /orders/`
  Cria pedido para o usuario autenticado.
- `POST /orders/pedido/cancelar/{id_pedido}`
  Cancela pedido proprio ou qualquer pedido, se admin.
- `POST /orders/pedido/{id_pedido}/items`
  Adiciona item ao pedido e recalcula o total.
- `DELETE /orders/pedido/item/{id_item_pedido}`
  Remove item do pedido e recalcula o total.

## Exemplo de uso

### Criar usuario

```bash
curl -X POST http://127.0.0.1:8000/auth/Cadastrar ^
  -H "Content-Type: application/json" ^
  -d "{\"nome\":\"admin\",\"email\":\"admin@email.com\",\"senha\":\"123456\",\"ativo\":true,\"admin\":true}"
```

### Fazer login

```bash
curl -X POST http://127.0.0.1:8000/auth/Login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@email.com\",\"senha\":\"123456\"}"
```

### Criar pedido autenticado

```bash
curl -X POST http://127.0.0.1:8000/orders/ ^
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" ^
  -H "Content-Type: application/json" ^
  -d "{\"status\":\"Pendente\",\"preco\":0}"
```

### Adicionar item ao pedido

```bash
curl -X POST http://127.0.0.1:8000/orders/pedido/1/items ^
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" ^
  -H "Content-Type: application/json" ^
  -d "{\"quantidade\":2,\"sabor\":\"calabresa\",\"preco_unitario\":25.0}"
```

## Testes e validacoes

Para validacao rapida de sintaxe:

```bash
python -m py_compile main.py ordens.py schemas.py models.py autenticacao.py dependencias.py security.py
```

Para testar o carregamento da aplicacao:

```bash
python -c "from main import app; print(app.title)"
```

Para rodar a suite de testes quando houver testes implementados:

```bash
pytest -q
```

## Observacoes tecnicas

- O banco padrao atual e `SQLite` em arquivo local `database.db`.
- O projeto chama `Base.metadata.create_all(bind=db)` na importacao de `models.py`.
- Existe configuracao do Alembic no repositorio, mas o modelo atual ainda cria tabelas diretamente em runtime.
- A autenticacao usa `OAuth2PasswordBearer(tokenUrl="/auth/Login_form")`, o que integra o Swagger com login por formulario.
- O refresh token e diferenciado pelo campo `type` no payload JWT.

## Melhorias recomendadas

- substituir `create_all` por migracoes exclusivas via Alembic;
- normalizar nomes de funcoes e rotas para padrao snake_case / lowercase;
- adicionar testes automatizados para auth e pedidos;
- separar configuracoes em classe `Settings`;
- adicionar relacao explicita entre `Usuario` e `Pedido` no ORM;
- padronizar mensagens e textos em UTF-8 sem problemas de encoding.
