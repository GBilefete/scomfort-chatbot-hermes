# chatbot_app.py
# Requisitos: pip install streamlit openai pandas

import streamlit as st
import pandas as pd
import openai

# === CONFIGURACOES GERAIS ===
st.set_page_config(page_title="Chat de Recomendação - SComfort", page_icon="👟")
st.title("👟 Chat de Recomendação Personalizada da SComfort")
st.markdown("""
Bem-vindo! Responda algumas perguntas abaixo e receba uma recomendação personalizada
do nosso atendente virtual com inteligência artificial. Ideal para descobrir qual 
tênis é perfeito para o seu estilo! 💬
""")

# === API KEY ===
openai.api_key = st.secrets["openai"]["api_key"]

# === CARREGAR DADOS ===
clientes_df = pd.read_csv("scomfort_clientes.csv")
produtos_df = pd.read_csv("scomfort_produtos.csv")

# === FUNCAO DE RECOMENDACAO ===
def recomendar_modelo(idade, profissao, estado, estilo_vida, cor_preferida):
    faixa_idade = (clientes_df['idade'] >= idade - 3) & (clientes_df['idade'] <= idade + 3)
    mesma_profissao = clientes_df['profissao'].str.lower() == profissao.lower()
    mesmo_estado = clientes_df['estado'].str.upper() == estado.upper()
    clientes_semelhantes = clientes_df[faixa_idade & mesma_profissao & mesmo_estado]

    if clientes_semelhantes.empty:
        modelo_recomendado = "Classic"
    else:
        modelo_recomendado = clientes_semelhantes['modelo_preferido'].mode().values[0]

    estilo = estilo_vida.lower()
    if "esportiv" in estilo:
        modelo_recomendado = "Runner"
    elif "casual" in estilo:
        modelo_recomendado = "Classic"
    elif "urbano" in estilo:
        modelo_recomendado = "Slip-on"

    produtos_modelo = produtos_df[produtos_df['modelo'] == modelo_recomendado]
    tamanho_mais_vendido = produtos_modelo.groupby('tamanho')['vendas_mes'].sum().idxmax()

    if cor_preferida:
        cores_disponiveis = produtos_modelo['cor'].str.lower().unique()
        if cor_preferida.lower() in cores_disponiveis:
            cor_escolhida = cor_preferida.title()
        else:
            cor_escolhida = produtos_modelo.groupby('cor')['avaliacao_media'].mean().idxmax()
    else:
        cor_escolhida = produtos_modelo.groupby('cor')['avaliacao_media'].mean().idxmax()

    return modelo_recomendado, cor_escolhida, tamanho_mais_vendido

# === FUNCAO PARA GERAR RESPOSTA COM GPT ===
def gerar_mensagem_personalizada(modelo, cor, tamanho, idade, profissao, estado, estilo_vida, cor_preferida):
    prompt = f"""
    Você é Hermes, inspirado no mensageiro dos deuses, o consultor virtual da marca SComfort, especializada em tênis confortáveis.
    rápido e cheio de estilo. Sua missão é ajudar clientes a encontrarem o tênis mais confortável
    e estiloso, com base nas informações que eles fornecem.

    Crie uma recomendação personalizada para um(a) cliente com o seguinte perfil:
    - Idade: {idade}
    - Profissão: {profissao}
    - Estado: {estado}
    - Estilo de vida: {estilo_vida}
    - Cor preferida: {cor_preferida if cor_preferida else "não informada"}

    Com base nesses dados, e na recomendação gerada pelo sistema:
    - Modelo: {modelo}
    - Cor: {cor}
    - Tamanho: {tamanho}

    Sua resposta deve ser:
    - Divertida, animada e simpática (Hermes é um atendente que ama o que faz!).
    - Clara e confiante, explicando por que essa sugestão combina com o cliente.
    - Inspiradora: pode usar emojis, frases criativas, expressões gregas divertidas ("Por Zeus!" ou "voando baixo com estilo").
    Não mencione que é uma IA ou chatbot, e fale como se fosse um consultor da loja, estiloso e empolgado.
"""
    resposta = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content

# === FORMULARIO STREAMLIT ===
with st.form("formulario_recomendacao"):
    idade = st.number_input("Qual sua idade?", min_value=10, max_value=100, step=1)
    profissao = st.text_input("Qual sua profissão?")
    estado = st.text_input("De qual estado você é? (ex: SP, RJ)")
    estilo = st.selectbox("Como descreveria seu estilo de vida?", ["Casual", "Esportivo", "Urbano", "Outro"])
    cor_pref = st.text_input("Tem alguma cor preferida de tênis? (opcional)")
    enviar = st.form_submit_button("Gerar Recomendacão")

# === GERAR RESULTADO ===
if enviar:
    with st.spinner("Analisando seu perfil e gerando sugestão..."):
        modelo, cor, tamanho = recomendar_modelo(idade, profissao, estado, estilo, cor_pref)
        mensagem = gerar_mensagem_personalizada(modelo, cor, tamanho, idade, profissao, estado, estilo, cor_pref)
        st.success("Recomendação gerada com sucesso!")
        st.markdown(f"### 📨 Resultado:\n{mensagem}")
