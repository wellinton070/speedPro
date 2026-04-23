from modulos.usuario import cadastrar_usuario, buscar_usuario
from modulos.treino import criar_plano, ajustar_plano_semanal
from modulos.feedback import registrar_feedback, ver_historico

def menu_inicial():
    print("\n=============================")
    print("   SISTEMA DE TREINO CORRIDA ")
    print("=============================")
    print("1 - Sou novo, quero me cadastrar")
    print("2 - Já tenho cadastro")
    print("0 - Sair")
    print("=============================")
    return input("Escolha uma opção: ")

def menu_principal(nome):
    print(f"\n=== Olá, {nome}! ===")
    print("1 - Gerar novo plano de treino")
    print("2 - Registrar treino realizado")
    print("3 - Ver histórico de treinos")
    print("4 - Ajustar plano com base no histórico")
    print("0 - Sair")
    print("=============================")
    return input("Escolha uma opção: ")

def main():
    usuario = None

    while usuario is None:
        opcao = menu_inicial()

        if opcao == "1":
            usuario = cadastrar_usuario()

        elif opcao == "2":
            id_digitado = int(input("\nDigite seu ID de usuário: "))
            usuario = buscar_usuario(id_digitado)

        elif opcao == "0":
            print("\nAté logo!")
            return

        else:
            print("\nOpção inválida, tente novamente.")

    id_plano = None

    while True:
        opcao = menu_principal(usuario["nome"])

        if opcao == "1":
            id_plano = criar_plano(usuario)

        elif opcao == "2":
            if id_plano is None:
                print("\nVocê precisa gerar um plano primeiro!")
            else:
                registrar_feedback(usuario["id"], id_plano)

        elif opcao == "3":
            ver_historico(usuario["id"])

        elif opcao == "4":
            id_plano = ajustar_plano_semanal(usuario)

        elif opcao == "0":
            print("\nAté logo!")
            break

        else:
            print("\nOpção inválida, tente novamente.")

main()