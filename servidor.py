from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.modelos import criar_tabelas
from api.rotas_usuario import router as router_usuario
from api.rotas_treino import router as router_treino

app = FastAPI(
    title="Sistema de Treino para Corredores",
    description="API para acompanhamento inteligente de treinos de corrida",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

criar_tabelas()

app.include_router(router_usuario)
app.include_router(router_treino)

@app.get("/")
def inicio():
    return {"mensagem": "API de Treino para Corredores funcionando!"}