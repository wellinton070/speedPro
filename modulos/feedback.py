from database.conexao import conectar

def registrar_feedback(id_usuario, id_plano):
    print("\n=== REGISTRO DE TREINO ===\n")

    data = input("Data do treino (ex: 2026-04-18): ")
    tipo = input("Tipo de treino realizado: ")
    duracao = int(input("Duração em minutos: "))
    distancia = float(input("Distância percorrida em km: "))
    cansaco = int(input("Nível de cansaço de 1 a 10: "))
    observacoes = input("Alguma observação ou dor? (ou 'nenhuma'): ")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO sessoes_treino 
        (id_usuario, id_plano, data_treino, tipo_treino, duracao_min, distancia_km, nivel_cansaco, observacoes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (id_usuario, id_plano, data, tipo, duracao, distancia, cansaco, observacoes))

    conexao.commit()
    cursor.close()
    conexao.close()

    print("\nTreino registrado com sucesso!")

def ver_historico(id_usuario):
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

    if not sessoes:
        print("\nVocê ainda não registrou nenhum treino!")
        return

    print("\n===== SEU HISTÓRICO DE TREINOS =====\n")
    for sessao in sessoes:
        print(f"Data: {sessao[0]}")
        print(f"Tipo: {sessao[1]}")
        print(f"Duração: {sessao[2]} minutos")
        print(f"Distância: {sessao[3]} km")
        print(f"Cansaço: {sessao[4]}/10")
        print(f"Observações: {sessao[5]}")
        print("------------------------------------")