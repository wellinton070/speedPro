from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

cliente = Groq(api_key=os.getenv("GEMINI_API_KEY"))

def gerar_plano(usuario):
    prompt = f"""
    Você é um personal trainer especializado em corrida para iniciantes.
    Com base nos dados abaixo, crie um plano de treino semanal detalhado:

    - Nome: {usuario['nome']}
    - Idade: {usuario['idade']} anos
    - Peso: {usuario['peso']} kg
    - Altura: {usuario['altura']} cm
    - Nível: {usuario['nivel']}
    - Objetivo: {usuario['objetivo']}
    - Dias disponíveis por semana: {usuario['dias_disponiveis']}
    - Lesões ou restrições: {usuario['lesoes']}

    O plano deve incluir para cada dia: tipo de treino, duração ou distância,
    intensidade e dicas de aquecimento. Priorize a prevenção de lesões.
    """

    resposta = cliente.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content

def ajustar_plano(usuario, historico):
    prompt = f"""
    Você é um personal trainer especializado em corrida para iniciantes.
    O atleta abaixo já treinou por uma semana e precisa de um plano ajustado.

    Dados do atleta:
    - Nome: {usuario['nome']}
    - Nível: {usuario['nivel']}
    - Objetivo: {usuario['objetivo']}
    - Dias disponíveis: {usuario['dias_disponiveis']}

    Histórico da semana anterior:
    {historico}

    Com base no histórico acima, analise o nível de cansaço, as observações
    e o desempenho do atleta. Gere um novo plano semanal ajustado, aumentando
    ou reduzindo a intensidade conforme necessário. Priorize a prevenção de lesões.
    """

    resposta = cliente.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content