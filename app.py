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
    .main-title { font-size: 42px; font-weight: 800; color: #0D1B2A; margin-bottom: 10px; }
    .sub-title { font-size: 18px; color: #415A77; margin-bottom: 30px; }
    .product-header { 
        background: linear-gradient(90deg, #0077b6, #00b4d8); 
        color: white; 
        padding: 20px; 
        border-radius: 10px; 
        margin-bottom: 25px; 
    }
    .stButton > button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3.5em; 
        font-weight: bold; 
        background-color: #0077b6;
        color: white;
        border: none;
    }
    .stButton > button:hover {
        background-color: #00b4d8;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DA API ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 4. INICIALIZAÇÃO DO ESTADO DE SESSÃO (MEMÓRIA DAS TAGS) ---
if 'tags_disponiveis' not in st.session_state:
    st.session_state.tags_disponiveis = ["Novas Leis", "Concorrência", "Inovação", "Macroeconomia", "Dólar", "Tributação"]

# --- 5. BARRA LATERAL (NAVEGAÇÃO) ---
with st.sidebar:
    st.title("⚡ TechnoBolt IA")
    st.markdown("---")
    menu = st.radio(
        "Escolha a Ferramenta:",
        ["Página Inicial", "Gerador de Email Inteligente", "Gerador de Briefing Negocial"]
    )
    st.markdown("---")
    if not api_key:
        st.error("⚠️ API Key não encontrada.")
    st.caption(f"v1.5.0 | Dezembro 2025")

# --- 6. LÓGICA DAS PÁGINAS ---

# --- TELA: PÁGINA INICIAL ---
if menu == "Página Inicial":
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Hub estratégico de produtividade movido por Inteligência Artificial de última geração.</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🚀 Bem-vindo ao seu ecossistema de IA
    Nossas ferramentas foram desenvolvidas para acelerar processos executivos e criativos.
    
    * **✉️ Gerador de Email Inteligente:** Crie comunicações profissionais definindo o cargo e o objetivo.
    * **🧠 Gerador de Briefing Negocial:** Radar estratégico com notícias de última hora baseado em tags livres.
    
    ---
    *Selecione uma opção no menu ao lado para começar.*
    """)

# --- TELA: GERADOR DE EMAIL INTELIGENTE ---
elif menu == "Gerador de Email Inteligente":
    st.markdown('<div class="product-header">✉️ Gerador de Email Inteligente</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        cargo_ia = st.text_input("Qual cargo a IA deve assumir?", placeholder="Ex: Diretor Financeiro, Gerente de Vendas...")
        destinatario = st.text_input("Para quem você está escrevendo?", placeholder="Ex: CEO da Empresa X, Novo Cliente...")
        objetivo = st.text_area("O que você deseja com esse e-mail? (Objetivo)", placeholder="Ex: Solicitar proposta, agendar reunião...")
        tom = st.select_slider("Nível de Formalidade:", options=["Muito Casual", "Cordial/Amigável", "Executivo/Sério", "Urgente/Direto"])
    
    with col2:
        st.markdown("### ✨ Resultado")
        if st.button("🚀 CRIAR E-MAIL COM IA"):
            if not cargo_ia or not objetivo:
                st.warning("Preencha o cargo e o objetivo.")
            else:
                with st.spinner("Redigindo comunicação..."):
                    try:
                        model = genai.GenerativeModel("models/gemini-3-flash-preview")
                        prompt = f"Atue como um {cargo_ia}. Escreva um e-mail para {destinatario} focado em {objetivo}. Tom: {tom}."
                        response = model.generate_content(prompt)
                        st.text_area("Cópia disponível:", response.text, height=400)
                    except Exception as e:
                        st.error(f"Erro: {e}")

# --- TELA: GERADOR DE BRIEFING NEGOCIAL ---
elif menu == "Gerador de Briefing Negocial":
    st.markdown('<div class="product-header">🧠 Gerador de Briefing Negocial</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        empresa = st.text_input("Sua Organização:", placeholder="Ex: TechnoBolt Tech")
        setor = st.text_input("Setor de Atuação:", placeholder="Ex: Logística, Agronegócio...")
        
        # --- SISTEMA DE TAGS DINÂMICAS ---
        tags_selecionadas = st.multiselect(
            "Prioridades do Radar (Selecione ou crie abaixo):",
            options=st.session_state.tags_disponiveis,
            default=["Novas Leis"]
        )
        
        # Campo para criar novas tags
        nova_tag = st.text_input("➕ Digite uma nova tag e aperte Enter:", placeholder="Ex: Concorrente X")
        if nova_tag and nova_tag not in st.session_state.tags_disponiveis:
            st.session_state.tags_disponiveis.append(nova_tag)
            st.rerun()

    with col2:
        st.markdown("### 📊 Radar de Notícias & Insights")
        if st.button("⚡ ESCANEAR MERCADO"):
            if not empresa or not setor:
                st.warning("Preencha empresa e setor.")
            else:
                with st.spinner("IA processando notícias de última hora..."):
                    try:
                        model = genai.GenerativeModel("models/gemini-3-flash-preview")
                        tags_str = ", ".join(tags_selecionadas)
                        prompt_b = f"""
                        Atue como Chief Strategy Officer. Data: {time.strftime('%d/%m/%Y')}.
                        Gere um briefing para a empresa {empresa} no setor de {setor}.
                        Foco exclusivo nas Tags de Radar: {tags_str}.

                        ESTRUTURA:
                        1. 🚩 RADAR DE NOTÍCIAS (Eventos reais de última hora sobre as tags).
                        2. 📉 IMPACTO NO NEGÓCIO (Consequências para a {empresa}).
                        3. 💡 RECOMENDAÇÃO EXECUTIVA.
                        """
                        response = model.generate_content(prompt_b)
                        st.markdown(response.text)
                        st.download_button("📥 Baixar Relatório", response.text, file_name=f"Briefing_{empresa}.md")
                    except Exception as e:
                        st.error(f"Erro: {e}")

# --- 7. RODAPÉ ---
st.markdown("---")
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Inteligência Artificial Corporativa")