import streamlit as st
import google.generativeai as genai
import os
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="TechnoBolt IA - Hub Corporativo",
    page_icon="⚡",
    layout="wide"
)

# --- 2. CSS PARA DESIGN PREMIUM ---
st.markdown("""
<style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #ffffff; color: #1e1e1e; }
    .sidebar .sidebar-content { background-color: #f8f9fa; }
    .main-title { font-size: 42px; font-weight: 800; color: #0D1B2A; margin-bottom: 10px; }
    .sub-title { font-size: 18px; color: #415A77; margin-bottom: 30px; }
    .product-header { background: linear-gradient(90deg, #0077b6, #00b4d8); color: white; padding: 20px; border-radius: 10px; margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DA API ---
# Recomendação: Use variável de ambiente ou cole sua chave aqui
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 4. BARRA LATERAL (NAVEGAÇÃO DO HUB) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=80) # Ícone decorativo IA
    st.title("TechnoBolt IA")
    st.markdown("---")
    
    st.subheader("🛠️ Ferramentas")
    menu = st.radio(
        "Selecione a solução:",
        ["Home", "Gerador de Email Inteligente", "Gerador de Briefing Negocial"],
        index=0
    )
    
    st.markdown("---")
    st.caption("Powered by Gemini 3 Flash & 2.5 Flash")
    st.caption("v1.0.0 - 2025 Edition")

# --- 5. LÓGICA DAS PÁGINAS ---

# --- TELA HOME ---
if menu == "Home":
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">O Hub definitivo de produtividade corporativa potencializado por Inteligência Artificial de última geração.</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🚀 O que é o TechnoBolt IA?
    Nossa plataforma centraliza as capacidades mais avançadas de IA para acelerar sua tomada de decisão e comunicação. 
    **Tudo aqui faz uso de modelos generativos de ponta** para garantir que você esteja sempre um passo à frente do mercado.

    ---
    #### Nossas Soluções Atuais:
    
    * **✉️ Gerador de Email Inteligente:** Transforme intenções simples em comunicações persuasivas e profissionais para clientes e parceiros em segundos.
    * **🧠 Gerador de Briefing Negocial:** Receba análises profundas do seu setor, tendências de 2025 e um radar de notícias críticas para a sua gestão.
    
    ---
    *Selecione uma ferramenta no menu ao lado para começar.*
    """)

# --- TELA: GERADOR DE EMAIL INTELIGENTE ---
elif menu == "Gerador de Email Inteligente":
    st.markdown('<div class="product-header">✉️ Gerador de Email Inteligente</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        destinatario = st.text_input("Para quem é o e-mail? (Ex: Diretor de Compras)")
        objetivo = st.text_area("Qual o objetivo principal?", placeholder="Ex: Marcar reunião de apresentação do software TechnoBolt")
        tom = st.select_slider("Tom de voz:", options=["Informal", "Cordial", "Executivo", "Urgente"])
    
    with col2:
        modelo = st.selectbox("Motor IA:", ["models/gemini-3-flash-preview", "models/gemini-2.0-flash"])
        if st.button("✨ GERAR E-MAIL COM IA"):
            with st.spinner("IA redigindo sua mensagem..."):
                try:
                    model = genai.GenerativeModel(modelo)
                    prompt_email = f"Atue como um redator profissional. Escreva um e-mail para {destinatario} com o objetivo: {objetivo}. O tom deve ser {tom}. Formate com Assunto e Corpo."
                    response = model.generate_content(prompt_email)
                    st.info(response.text)
                except Exception as e:
                    st.error(f"Erro: {e}")

# --- TELA: GERADOR DE BRIEFING NEGOCIAL ---
elif menu == "Gerador de Briefing Negocial":
    st.markdown('<div class="product-header">🧠 Gerador de Briefing Negocial</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        empresa = st.text_input("Sua Organização:", placeholder="Ex: Super Rodrigues")
        setor = st.text_input("Setor de Atuação:", placeholder="Ex: Varejo Alimentar")
        foco = st.multiselect("Prioridades do Radar:", ["Leis", "Concorrência", "Tecnologia", "Economia"], default=["Leis", "Tecnologia"])
        modelo_b = st.selectbox("Motor IA:", ["models/gemini-3-flash-preview", "models/gemini-2.5-flash"])
    
    with col2:
        if st.button("⚡ ESCANEAR MERCADO E NOTÍCIAS"):
            if not empresa or not setor:
                st.warning("Por favor, preencha os dados da empresa.")
            else:
                with st.spinner("IA processando dados estratégicos e notícias de Dezembro de 2025..."):
                    try:
                        model = genai.GenerativeModel(modelo_b)
                        prompt_briefing = f"""
                        Atue como Chief Strategy Officer. Data: Dezembro de 2025.
                        Gere um Briefing para a empresa {empresa} do setor {setor}.
                        
                        ESTRUTURA:
                        1. RADAR DE NOTÍCIAS DE ÚLTIMA HORA (Fatos reais de Dez/2025 no Brasil sobre {setor}).
                        2. ANÁLISE DE TENDÊNCIAS E IMPACTO (Foco em {foco}).
                        3. RECOMENDAÇÃO EXECUTIVA PARA O CEO.
                        
                        Responda em Português de forma profissional.
                        """
                        response = model.generate_content(prompt_briefing)
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Erro: {e}")

# --- RODAPÉ COMUM ---
st.markdown("---")
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Todos os processos protegidos por IA.")