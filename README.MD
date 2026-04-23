# SpeedPro - Sistema Inteligente de Treinos para Corredores

Aplicação web com Inteligência Artificial para acompanhamento personalizado de treinos de corrida.

## Tecnologias utilizadas

- Python 3.11+
- FastAPI
- PostgreSQL
- Groq API (IA - modelo LLaMA 3.3 70B)
- HTML, CSS e JavaScript

## Como rodar o projeto

### 1. Clone o repositório
git clone https://github.com/wellinton070/speedPro.git
cd speedPro

### 2. Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate

### 3. Instale as dependências
pip install -r requirements.txt

### 4. Configure o arquivo .env
Crie um arquivo .env na raiz do projeto com:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=nome_do_banco
DB_USER=postgres
DB_PASSWORD=sua_senha
GEMINI_API_KEY=sua_chave_groq

### 5. Suba a API
uvicorn servidor:app --reload

### 6. Abra o frontend
Abra o arquivo corrida-web/index.html no navegador

## Funcionalidades

- Cadastro de usuário em 3 etapas
- Login com email e senha
- Geração de plano de treino personalizado com IA
- Ajuste adaptativo do plano com base no histórico
- Registro de treinos realizados
- Histórico completo de treinos