# Sistema de Treino para Corredores

Aplicação em Python com IA para acompanhamento de treinos de corrida.

## Como rodar o terminal

1. Ative o ambiente virtual: source venv/bin/activate
2. Instale as dependências: pip install -r requirements.txt
3. Configure o arquivo .env com suas credenciais
4. Execute: python3 main.py

## Como rodar a API

1. Execute: uvicorn servidor:app --reload
2. Acesse: http://127.0.0.1:8000/docs