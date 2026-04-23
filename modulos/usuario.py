from database.conexao import conectar

def cadastrar_usuario():
    print("\n=== CADASTRO DE USUÁRIO ===\n")

    nome = input("Qual é o seu nome? ")
    idade = int(input("Qual é a sua idade? "))
    peso = float(input("Qual é o seu peso em kg? "))
    altura = float(input("Qual é a sua altura em cm? "))

    print("\nNível de experiência:")
    print("1 - Nunca corri")
    print("2 - Corro raramente")
    print("3 - Corro com frequência")
    nivel_opcao = input("Escolha uma opção (1, 2 ou 3): ")

    niveis = {"1": "iniciante", "2": "intermediário", "3": "avançado"}
    nivel = niveis.get(nivel_opcao, "iniciante")

    objetivo = input("\nQual é o seu objetivo? (ex: correr 5km, emagrecer): ")
    dias = int(input("Quantos dias por semana você pode treinar? "))
    lesoes = input("Tem alguma lesão ou restrição física? (ou digite 'nenhuma'): ")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO usuarios (nome, idade, peso, altura, nivel, objetivo, dias_disponiveis, lesoes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (nome, idade, peso, altura, nivel, objetivo, dias, lesoes))

    id_usuario = cursor.fetchone()[0]
    conexao.commit()
    cursor.close()
    conexao.close()

    print(f"\nUsuário cadastrado com sucesso! Seu ID é: {id_usuario}")

    return {
        "id": id_usuario,
        "nome": nome,
        "idade": idade,
        "peso": peso,
        "altura": altura,
        "nivel": nivel,
        "objetivo": objetivo,
        "dias_disponiveis": dias,
        "lesoes": lesoes
    } 
def buscar_usuario(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, idade, peso, altura, nivel, objetivo, dias_disponiveis, lesoes
        FROM usuarios
        WHERE id = %s
    """, (id_usuario,))

    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()

    if resultado is None:
        print("\nUsuário não encontrado!")
        return None

    usuario = {
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

    print(f"\nBem-vindo de volta, {usuario['nome']}!")
    return usuario