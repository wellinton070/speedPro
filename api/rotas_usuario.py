from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from modulos.usuario import buscar_usuario
from database.conexao import conectar

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

class UsuarioEntrada(BaseModel):
    nome: str
    idade: int
    peso: float
    altura: float
    nivel: str
    objetivo: str
    dias_disponiveis: int
    lesoes: str
    email: str
    senha: str

class LoginEntrada(BaseModel):
    email: str
    senha: str

@router.post("/login")
def login(dados: LoginEntrada):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, idade, peso, altura, nivel, objetivo, dias_disponiveis, lesoes
        FROM usuarios
        WHERE email = %s AND senha = %s
    """, (dados.email, dados.senha))

    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()

    if resultado is None:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos!")

    return {
        "id": resultado[0],
        "nome": resultado[1],
        "idade": resultado[2],
        "peso": resultado[3],
        "altura": resultado[4],
        "nivel": resultado[5],
        "objetivo": resultado[6],
        "dias_disponiveis": resultado[7],
        "lesoes": resultado[8]
    }

@router.post("/")
def criar_usuario(usuario: UsuarioEntrada):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO usuarios (nome, idade, peso, altura, nivel, objetivo, dias_disponiveis, lesoes, email, senha)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (usuario.nome, usuario.idade, usuario.peso, usuario.altura,
          usuario.nivel, usuario.objetivo, usuario.dias_disponiveis, usuario.lesoes,
          usuario.email, usuario.senha))

    id_usuario = cursor.fetchone()[0]
    conexao.commit()
    cursor.close()
    conexao.close()

    return {"id": id_usuario, "mensagem": f"Usuário {usuario.nome} cadastrado com sucesso!"}

@router.get("/{id_usuario}")
def obter_usuario(id_usuario: int):
    usuario = buscar_usuario(id_usuario)

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario