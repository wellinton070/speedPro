# ============================================================
# ia/gemini.py — Módulo de Inteligência Artificial
# Suporta dois provedores de IA:
#   1. Groq direto (implementação original — sem LangChain)
#   2. LangChain + Gemini (nova implementação com framework LangChain)
# ============================================================

from groq import Groq
import os
from dotenv import load_dotenv

# --- Imports do LangChain ---
# LangChain é um framework que padroniza como trabalhar com diferentes IAs
from langchain_google_genai import ChatGoogleGenerativeAI  # Conector LangChain → Gemini
from langchain_core.prompts import ChatPromptTemplate       # Template de prompts

load_dotenv()

# ============================================================
# CLIENTE GROQ DIRETO (implementação original — sem alterações)
# Usa a biblioteca oficial do Groq sem nenhum framework
# ============================================================
cliente_groq = Groq(api_key=os.getenv("API_KEY_GROQ"))

# ============================================================
# CLIENTE LANGCHAIN + GEMINI (nova implementação com framework)
# ChatGoogleGenerativeAI é a classe do LangChain que conecta ao Gemini
# temperature=0.7 controla a criatividade (0=preciso, 1=criativo)
# ============================================================
cliente_gemini = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=os.getenv("API_KEY_GEMINI"),
    temperature=0.7
)


def extrair_conteudo(resposta):
    """
    Extrai o texto da resposta do LangChain.
    O Gemini retorna content como lista de dicts com chave 'text'.
    """
    conteudo = resposta.content
    if isinstance(conteudo, list):
        partes = []
        for parte in conteudo:
            if isinstance(parte, dict) and 'text' in parte:
                partes.append(parte['text'])
            else:
                partes.append(str(parte))
        return '\n'.join(partes)
    elif isinstance(conteudo, dict) and 'text' in conteudo:
        return conteudo['text']
    return str(conteudo)

# ============================================================
# FUNÇÃO: gerar_plano
# Gera um plano de treino semanal personalizado
# provedor="groq"   → usa Groq direto (original)
# provedor="gemini" → usa LangChain + Gemini (framework)
# ============================================================
def gerar_plano(usuario, provedor="groq"):

    texto_prompt = f"""
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

    if provedor == "gemini":
        # --- IMPLEMENTAÇÃO LANGCHAIN + GEMINI ---
        # ChatPromptTemplate cria um template reutilizável de prompt
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Você é um personal trainer especializado em corrida para iniciantes."),
            ("human", "{conteudo}")
        ])

        # O operador | (pipe) conecta o prompt ao modelo — cria uma "chain"
        chain = prompt_template | cliente_gemini

        # .invoke() executa a chain substituindo {conteudo} pelo texto real
        resposta = chain.invoke({"conteudo": texto_prompt})

        # extrair_conteudo garante que retornamos sempre uma string
        return extrair_conteudo(resposta)

    else:
        # --- IMPLEMENTAÇÃO GROQ DIRETA (original — sem alterações) ---
        resposta = cliente_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": texto_prompt}]
        )
        return resposta.choices[0].message.content


# ============================================================
# FUNÇÃO: ajustar_plano
# Ajusta o plano com base no histórico de treinos do usuário
# provedor="groq"   → usa Groq direto (original)
# provedor="gemini" → usa LangChain + Gemini (framework)
# ============================================================
def ajustar_plano(usuario, historico, provedor="groq"):

    texto_prompt = f"""
    Você é um personal trainer especializado em corrida para iniciantes.
    O usuário {usuario['nome']} seguiu o plano por um tempo. Com base no histórico abaixo,
    ajuste e melhore o plano de treino:
    Histórico de feedbacks: {historico}
    Nível atual: {usuario['nivel']}
    Objetivo: {usuario['objetivo']}
    Crie um plano ajustado considerando o progresso e dificuldades relatadas.
    """

    if provedor == "gemini":
        # --- IMPLEMENTAÇÃO LANGCHAIN + GEMINI ---
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Você é um personal trainer especializado em corrida para iniciantes."),
            ("human", "{conteudo}")
        ])

        # Mesma chain: prompt → gemini → resposta
        chain = prompt_template | cliente_gemini
        resposta = chain.invoke({"conteudo": texto_prompt})

        # extrair_conteudo garante que retornamos sempre uma string
        return extrair_conteudo(resposta)

    else:
        # --- IMPLEMENTAÇÃO GROQ DIRETA (original — sem alterações) ---
        resposta = cliente_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": texto_prompt}]
        )
        return resposta.choices[0].message.content