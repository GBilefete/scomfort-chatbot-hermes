# 👟 SComfort Hermes Chatbot

Bem-vindo ao **Hermes**, o consultor virtual da **SComfort – O Tênis Mais Confortável do Mundo!**  
Inspirado no mensageiro dos deuses da mitologia grega, o Hermes é rápido, estiloso e está sempre pronto para te ajudar a escolher o tênis perfeito para seu perfil!

---

## 🌐 Demonstração Online

🔗 [Acesse o app ao vivo aqui](https://scomfort-hermes-chatbot.streamlit.app/)

---

## 🤖 Sobre o Projeto

Este projeto foi desenvolvido como trabalho final da disciplina de **Inteligência Artificial**, com o objetivo de aplicar IA Generativa em uma solução prática e integrada a uma interface visual.

A solução é um chatbot inteligente que interage com o cliente de forma divertida e personalizada, utilizando dados como:

- Idade  
- Profissão  
- Estado  
- Estilo de vida  
- Cor preferida

O sistema cruza esses dados com a base de clientes da SComfort, aplicando técnicas simples de filtragem. A partir dessa análise, ele recomenda o modelo de tênis mais adequado ao perfil do usuário.

Com base nesses dados, o sistema consulta um modelo de recomendação e, via **OpenAI GPT-3.5**, gera mensagens empolgantes que simulam o atendimento de um consultor animado e confiante, inspirado no mensageiro dos deuses da mitologia grega.

---

## 🔍 Funcionalidades

- 🧠 Recomendação de tênis com base em dados do usuário
- 🤖 Geração de respostas criativas com linguagem natural
- 🎨 Interface personalizada com imagem do Hermes e design responsivo
- 🚀 Hospedagem no Streamlit Cloud
- 🔐 Chave da API protegida via `secrets.toml`

---

## 💻 Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [OpenAI GPT-3.5](https://platform.openai.com/)
- [Pandas](https://pandas.pydata.org/)
- [Git + GitHub](https://github.com/)

---

## ⚙️ Como Executar Localmente

1. **Clone o repositório:**

```bash
git clone https://github.com/GBilefete/scomfort-hermes-chatbot.git
cd scomfort-hermes-chatbot
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Crie o arquivo .streamlit/secrets.toml com sua chave da OpenAI:**
```ini
[openai]
api_key = "sua-chave-aqui"
```

⚠️ Nunca suba esse arquivo para o GitHub público.

4. **Execute a aplicação:**

```bash
streamlit run app/chatbot_hermes_app.py
```

---

## 📁 Organização do Projeto

```csharp
scomfort-chatbot-hermes/
├── app/
│   └── chatbot_hermes_app.py         # App principal em Streamlit
├── data/
│   ├── scomfort_clientes.csv
│   ├── scomfort_produtos.csv
├── images/
│   ├── hermes.png                    # Imagem do assistente
│   ├── classic.png
│   ├── runner.png
│   ├── slip-on.png
├── site/
│   ├── index.html                    # Página inicial da marca, CSS, imagens, etc.
├── .streamlit/
│   └── secrets.toml                  # Chave da API (local, não subir)
├── requirements.txt
└── README.md

```

---

## 👨‍💻 Autor
Desenvolvido por Gerald Bilefete.











