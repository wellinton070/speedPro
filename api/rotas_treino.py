from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from modulos.treino import criar_plano, ajustar_plano_semanal
from modulos.feedback import registrar_feedback, ver_historico
from modulos.usuario import buscar_usuario

router = APIRouter(prefix="/treinos", tags=["Treinos"])

class FeedbackEntrada(BaseModel):
    id_usuario: int
    id_plano: int
    data_treino: str
    tipo_treino: str
    duracao_min: int
    distancia_km: float
    nivel_cansaco: int
    observacoes: str

@router.post("/plano/{id_usuario}")
def gerar_plano(id_usuario: int):
    usuario = buscar_usuario(id_usuario)

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    id_plano = criar_plano(usuario)
    return {"id_plano": id_plano, "mensagem": "Plano gerado com sucesso!"}

@router.post("/feedback")
def salvar_feedback(feedback: FeedbackEntrada):
    from database.conexao import conectar

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO sessoes_treino
        (id_usuario, id_plano, data_treino, tipo_treino, duracao_min, distancia_km, nivel_cansaco, observacoes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (feedback.id_usuario, feedback.id_plano, feedback.data_treino,
          feedback.tipo_treino, feedback.duracao_min, feedback.distancia_km,
          feedback.nivel_cansaco, feedback.observacoes))

    conexao.commit()
    cursor.close()
    conexao.close()

    return {"mensagem": "Treino registrado com sucesso!"}

@router.get("/historico/{id_usuario}")
def historico(id_usuario: int):
    from database.conexao import conectar

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT data_treino, tipo_treino, duracao_min, distancia_km, nivel_cansaco, observacoes
        FROM sessoes_treino
        WHERE id_usuario = %s
        ORDER BY data_treino DESC
    """, (id_usuario,))

    sessoes = cursor.fetchall()
    cursor.close()
    conexao.close()

    return [
        {
            "data": str(s[0]),
            "tipo": s[1],
            "duracao_min": s[2],
            "distancia_km": s[3],
            "nivel_cansaco": s[4],
            "observacoes": s[5]
        }
        for s in sessoes
    ]

@router.post("/ajustar/{id_usuario}")
def ajustar_plano(id_usuario: int):
    usuario = buscar_usuario(id_usuario)

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    id_plano = ajustar_plano_semanal(usuario)
    return {"id_plano": id_plano, "mensagem": "Plano ajustado com sucesso!"}

@router.get("/plano-conteudo/{id_plano}")
def buscar_conteudo_plano(id_plano: int):
    from database.conexao import conectar

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT conteudo FROM planos_treino WHERE id = %s
    """, (id_plano,))

    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()

    if resultado is None:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    return {"conteudo": resultado[0]}