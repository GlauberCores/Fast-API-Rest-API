## ⚙️ Funcionalidades
- Cadastro de usuários
- Autenticação
- Criação de pedidos
- Estrutura modular com rotas separadas

## ▶️ Como rodar o projeto

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPO.git
cd SEU_REPO

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload