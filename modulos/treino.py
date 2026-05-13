from database.conexao import conectar
from ia.gemini import gerar_plano, ajustar_plano

# --- Adicionamos o parâmetro 'provedor' nas duas funções ---
# Ele chega aqui vindo da rota da API e é repassado para a IA

def criar_plano(usuario, provedor="groq"):
    print("\nGerando seu plano de treino personalizado...")
    print(f"Aguarde, a IA está trabalhando... (usando: {provedor})\n")

    # Passa o provedor para a função de IA — ela decide qual usar
    plano = gerar_plano(usuario, provedor)

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO planos_treino (id_usuario, semana, conteudo)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (usuario["id"], 1, plano))

    id_plano = cursor.fetchone()[0]
    conexao.commit()
    cursor.close()
    conexao.close()

    print("===== SEU PLANO DE TREINO =====\n")
    print(plano)
    print("\n================================")
    print(f"Plano salvo no banco com ID: {id_plano}")

    return id_plano


def ajustar_plano_semanal(usuario, provedor="groq"):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT data_treino, tipo_treino, duracao_min, distancia_km, nivel_cansaco, observacoes
        FROM sessoes_treino
        WHERE id_usuario = %s
        ORDER BY data_treino DESC
        LIMIT 7
    """, (usuario["id"],))

    sessoes = cursor.fetchall()
    cursor.close()
    conexao.close()

    if not sessoes:
        print("\nVocê ainda não tem treinos registrados para ajustar o plano!")
        return None

    historico = ""
    for sessao in sessoes:
        historico += f"- Data: {sessao[0]}, Tipo: {sessao[1]}, Duração: {sessao[2]}min, "
        historico += f"Distância: {sessao[3]}km, Cansaço: {sessao[4]}/10, Obs: {sessao[5]}\n"

    print("\nAnalisando seu histórico e gerando plano ajustado...")
    print(f"Aguarde, a IA está trabalhando... (usando: {provedor})\n")

    # Passa o provedor para a função de IA — ela decide qual usar
    plano = ajustar_plano(usuario, historico, provedor)

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM planos_treino WHERE id_usuario = %s
    """, (usuario["id"],))
    semana = cursor.fetchone()[0] + 1

    cursor.execute("""
        INSERT INTO planos_treino (id_usuario, semana, conteudo)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (usuario["id"], semana, plano))

    id_plano = cursor.fetchone()[0]
    conexao.commit()
    cursor.close()
    conexao.close()

    print("===== PLANO AJUSTADO =====\n")
    print(plano)
    print("\n==========================")
    print(f"Plano salvo no banco com ID: {id_plano}")

    return id_plano