# ============================================================
# ia/gemini.py — Módulo de Inteligência Artificial
# Suporta dois provedores de IA:
#   1. Groq direto (implementação original)
#   2. LangChain + Groq (nova implementação com framework LangChain)
# ============================================================

from groq import Groq
import os
from dotenv import load_dotenv

# --- Imports do LangChain ---
# LangChain é um framework que padroniza como trabalhar com diferentes IAs
from langchain_groq import ChatGroq                          # Conector LangChain → Groq
from langchain_core.prompts import ChatPromptTemplate        # Template de prompts

load_dotenv()

# ============================================================
# CLIENTE GROQ DIRETO (implementação original — sem alterações)
# ============================================================
cliente_groq = Groq(api_key=os.getenv("API_KEY_GROQ"))

# ============================================================
# CLIENTE LANGCHAIN + GROQ (nova implementação com framework)
# ChatGroq é a classe do LangChain que conecta ao Groq
# temperature=0.7 controla a criatividade (0=preciso, 1=criativo)
# ============================================================
cliente_langchain = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("API_KEY_GROQ"),
    temperature=0.7
)


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
        # --- IMPLEMENTAÇÃO LANGCHAIN ---
        # ChatPromptTemplate cria um template reutilizável de prompt
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Você é um personal trainer especializado em corrida para iniciantes."),
            ("human", "{conteudo}")
        ])

        # O operador | (pipe) conecta o prompt ao modelo — isso é uma "chain"
        chain = prompt_template | cliente_langchain

        # .invoke() executa a chain com os valores do placeholder
        resposta = chain.invoke({"conteudo": texto_prompt})

        # No LangChain a resposta vem em resposta.content
        return resposta.content

    else:
        # --- IMPLEMENTAÇÃO GROQ DIRETA (original) ---
        resposta = cliente_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": texto_prompt}]
        )
        return resposta.choices[0].message.content


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
        # --- IMPLEMENTAÇÃO LANGCHAIN ---
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Você é um personal trainer especializado em corrida para iniciantes."),
            ("human", "{conteudo}")
        ])

        chain = prompt_template | cliente_langchain
        resposta = chain.invoke({"conteudo": texto_prompt})
        return resposta.content

    else:
        # --- IMPLEMENTAÇÃO GROQ DIRETA (original) ---
        resposta = cliente_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": texto_prompt}]
        )
        return resposta.choices[0].message.content