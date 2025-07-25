# chatbot_hermes_app.py - Versão personalizada com visual Hermes/SComfort

import streamlit as st
import pandas as pd
import openai

# === CONFIG ===
st.set_page_config(page_title="Hermes - Consultor Virtual SComfort", page_icon="👟", layout="centered")

# === ESTILO PERSONALIZADO ===
# Define o tema personalizado para o aplicativo
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #e0f7fa 0%, #2AACB8 100%);
            color: #0A2342;
        }
        html, body, [class*="css"] {
            color: #0A2342;
        }
        .stMarkdown {
            color: #0A2342 !important;
        }
         label {
            color: #FFFFFF !important;
        }
        .st-emotion-cache-hjhvlk{
            background-color: #0A2342 !important;
            border-radius: 8px;
        }
        .stButton>button {
            background-color: #2AACB8 !important;
            color: #FFFFFF !important;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
        }
        .stButton>button:hover {
            background-color: #2396a2;
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            border-radius: 6px;
            border: 1px solid #2AACB8 !important;
            padding: 6px;
            background-color: #ffffff;
            color: #0A2342 !important;
        }
    </style>
""", unsafe_allow_html=True)

# === MAPEAMENTO DE MODELOS PARA IMAGENS ===
# Mapeia os modelos de tênis para suas respectivas imagens
modelos_imagem = {
    "Runner": "images/runner.png",
    "Classic": "images/classic.png",
    "Slip-on": "images/slip-on.png"
}

# === TÍTULO E LOGO ===
# st.image("images/hermes.png", width=180)
st.markdown("""
# 👟 Bem-vindo ao Hermes!
### O consultor virtual mais veloz e estiloso do Olimpo da SComfort ✨
Responda às perguntas abaixo e receba uma recomendação personalizada para voar baixo com muito conforto. 🚀
""")

# === OPENAI ===
openai.api_key = st.secrets["openai"]["api_key"]

# === DADOS ===
# Carrega os dados dos clientes e produtos
clientes_df = pd.read_csv("data/scomfort_clientes.csv")
produtos_df = pd.read_csv("data/scomfort_produtos.csv")

# === RECOMENDAR ===
# Filtra clientes semelhantes com base em: idade (faixa etária), profissão, estado estilo de vida, cor preferida (se informada).
def recomendar_modelo(idade, profissao, estado, estilo_vida, cor_preferida, tamanho):
    # Filtra clientes que estão em uma faixa de idade semelhante (até 3 anos para mais ou para menos)
    faixa_idade = (clientes_df['idade'] >= idade - 3) & (clientes_df['idade'] <= idade + 3)

    # Filtra clientes que têm a mesma profissão (ignora maiúsculas/minúsculas)
    mesma_profissao = clientes_df['profissao'].str.lower() == profissao.lower()

    # Filtra clientes do mesmo estado (ignora maiúsculas/minúsculas)
    mesmo_estado = clientes_df['estado'].str.upper() == estado.upper()

    # Combina os três filtros para encontrar clientes semelhantes:
    # mesma faixa etária, mesma profissão e mesmo estado
    clientes_semelhantes = clientes_df[faixa_idade & mesma_profissao & mesmo_estado]

    # Verifica se há clientes semelhantes (mesma faixa etária, profissão e estado)
    if not clientes_semelhantes.empty:
        # Se houver, seleciona o modelo mais popular entre eles
        # Usa o método mode() para encontrar o modelo mais frequente
        modelo_recomendado = clientes_semelhantes['modelo_preferido'].mode().values[0]
    else:
       # Se não houver clientes semelhantes, define um modelo padrão inicialmente
        modelo_recomendado = "Classic"

        # Usa o estilo de vida para refinar a recomendação
        estilo = estilo_vida.lower() # Transforma para minúsculas para facilitar a comparação
        
        # Se o estilo for esportivo, recomenda o modelo Runner
        if "esportiv" in estilo:
            modelo_recomendado = "Runner"
        # Se for casual, recomenda o Classic
        elif "casual" in estilo:
            modelo_recomendado = "Classic"
        # Se for urbano, recomenda o Slip-on
        elif "urbano" in estilo:
            modelo_recomendado = "Slip-on"

    # Filtra os dados dos produtos para obter as opções do modelo escolhido
    # Cria uma série booleana indicando quais linhas têm o modelo igual ao recomendado.
    # Cria um novo DataFrame (produtos_modelo) contendo apenas os dados do modelo escolhido.
    produtos_modelo = produtos_df[produtos_df['modelo'] == modelo_recomendado]
    
    # Usa o número do calçado informado pelo usuário
    tamanho_mais_adequado = tamanho

    if cor_preferida:
        cores_disponiveis = produtos_modelo['cor'].str.lower().unique()
        if cor_preferida.lower() in cores_disponiveis:
            cor_escolhida = cor_preferida.title()
        else:
            cor_escolhida = produtos_modelo.groupby('cor')['avaliacao_media'].mean().idxmax()
    else:
        cor_escolhida = produtos_modelo.groupby('cor')['avaliacao_media'].mean().idxmax()

    return modelo_recomendado, cor_escolhida, tamanho_mais_adequado

# === IA GENERATIVA ===
# Gera uma mensagem personalizada com base nas informações do cliente e na recomendação do modelo
def gerar_mensagem_personalizada(modelo, cor, tamanho, idade, profissao, estado, estilo_vida, cor_preferida):
    prompt = f"""
    Você é Hermes, inspirado no mensageiro dos deuses, o consultor virtual da marca SComfort, especializada em tênis confortáveis.
    Rápido e cheio de estilo. Sua missão é ajudar clientes a encontrarem o tênis mais confortável
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

# === FORMULÁRIO ===
# Cria o layout do aplicativo com duas colunas: uma para o Hermes e outra para o formulário
col1, col2 = st.columns([1, 2])  # lado esquerdo (Hermes), lado direito (formulário)

with col1:
    st.image("images/hermes.png", use_container_width=True)

with col2:
    with st.form("formulario"):
        idade = st.number_input("1️⃣ Qual a sua idade?", min_value=10, max_value=100)
        profissao = st.text_input("2️⃣ Qual a sua profissão?")
        estado = st.selectbox("3️⃣ De qual estado você é?", ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"])
        estilo = st.selectbox("4️⃣ Como descreveria seu estilo de vida?", ["Casual", "Esportivo", "Urbano", "Outro"])
        cor_pref = st.text_input("5️⃣ Tem alguma cor preferida de tênis? (opcional)")
        tamanho = st.selectbox("6️⃣ Qual o seu tamanho de calçado?", list(range(35, 45)))
        submit = st.form_submit_button("🎯 Receber Recomendação")

# === PROCESSAMENTO ===
# Quando o usuário clica no botão de enviar, processa as informações e gera a recomendação
if submit:
    with st.spinner("Hermes está voando até o Olimpo dos dados..."):
        modelo, cor, tamanho = recomendar_modelo(idade, profissao, estado, estilo, cor_pref, tamanho)
        mensagem = gerar_mensagem_personalizada(modelo, cor, tamanho, idade, profissao, estado, estilo, cor_pref)
        st.success("🏁 Recomendação pronta!")
        st.markdown("### 📩 Hermes diz:")
        st.markdown(mensagem)

        # Exibir imagem do modelo recomendado, se existir
        imagem_modelo = modelos_imagem.get(modelo)

        if imagem_modelo:
            st.image(imagem_modelo, caption=f"Modelo recomendado: {modelo}", use_container_width=True)

