import streamlit as st
import google.generativeai as genai
import os
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="TechnoBolt IA - Hub Corporativo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS AVANÇADO: CORREÇÃO DE VISIBILIDADE MOBILE E DESIGN ---
st.markdown("""
<style>
    /* 1. OCULTA ELEMENTOS PADRÃO DO STREAMLIT */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* 2. FORÇA A APARIÇÃO DO BOTÃO DA BARRA LATERAL (CÍRCULO AZUL) */
    /* Este seletor ataca o ID específico do componente de menu do Streamlit */
    [data-testid="stSidebarCollapseButton"] {
        background-color: #0077b6 !important;
        color: white !important;
        border-radius: 50% !important;
        width: 55px !important;
        height: 55px !important;
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        z-index: 9999999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.4) !important;
        visibility: visible !important;
    }
    
    /* Garante que o ícone da seta dentro do círculo seja branco e visível */
    [data-testid="stSidebarCollapseButton"] svg {
        fill: white !important;
        color: white !important;
        width: 35px !important;
        height: 35px !important;
    }

    /* 3. ESTILO GERAL DA INTERFACE */
    .stApp { background-color: #ffffff; color: #1e1e1e; }
    .main-title { font-size: 38px; font-weight: 800; color: #0D1B2A; margin-top: 10px; }
    .product-header { 
        background: linear-gradient(90deg, #0077b6, #00b4d8); 
        color: white; padding: 25px; border-radius: 12px; margin-bottom: 30px; 
    }
    
    /* 4. BOTÕES DE AÇÃO */
    .stButton > button { 
        width: 100%; border-radius: 10px; height: 3.8em; 
        font-weight: bold; background-color: #0077b6; color: white; border: none;
    }
    .stButton > button:hover {
        background-color: #00b4d8;
        transform: translateY(-2px);
    }

    /* 5. AVISO PARA MOBILE */
    @media (max-width: 768px) {
        .mobile-helper {
            background-color: #f0f2f6;
            border-left: 6px solid #0077b6;
            padding: 15px;
            margin-bottom: 25px;
            font-weight: 600;
            color: #0077b6;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DA API ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 4. MEMÓRIA DE SESSÃO (TAGS) ---
if 'tags_disponiveis' not in st.session_state:
    st.session_state.tags_disponiveis = ["Novas Leis", "Concorrência", "Inovação", "Macroeconomia"]

# --- 5. MENU LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("⚡ TechnoBolt IA")
    st.markdown("---")
    menu_selecionado = st.radio(
        "Selecione uma ferramenta:",
        ["Página Inicial", "Gerador de Email Inteligente", "Gerador de Briefing Negocial", "Analista de Atas de Governança"]
    )
    st.markdown("---")
    if not api_key:
        st.error("⚠️ API Key não configurada.")
    st.caption(f"v1.8.0 | Suíte Corporativa 2025")

# --- 6. FLUXO DE TELAS ---

# --- TELA: HOME ---
if menu_selecionado == "Página Inicial":
    st.markdown('<div class="mobile-helper">⬅️ Toque no círculo azul no topo para abrir o menu.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.write("##### Hub estratégico de produtividade corporativa potencializado por IA.")
    
    st.markdown("""
    ---
    ### 🛠️ Nossas Ferramentas:
    
    * **✉️ Gerador de Email Inteligente:** Redação executiva de alto nível.
    * **🧠 Gerador de Briefing Negocial:** Radar estratégico via tags personalizadas.
    * **📝 Analista de Atas de Governança:** Formalização instantânea de reuniões.
    
    ---
    *Utilize o menu lateral para começar.*
    """)

# --- TELA: EMAIL ---
elif menu_selecionado == "Gerador de Email Inteligente":
    st.markdown('<div class="product-header">✉️ Gerador de Email Inteligente</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2])
    with col1:
        cargo = st.text_input("Cargo que a IA deve assumir:")
        dest = st.text_input("Para quem você escreve?")
        obj = st.text_area("Objetivo do e-mail:")
    with col2:
        if st.button("🚀 GERAR E-MAIL"):
            with st.spinner("IA processando..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    res = model.generate_content(f"Como {cargo}, escreva para {dest} sobre {obj}.")
                    st.text_area("Resultado:", res.text, height=400)
                except Exception as e: st.error(f"Erro: {e}")

# --- TELA: BRIEFING ---
elif menu_selecionado == "Gerador de Briefing Negocial":
    st.markdown('<div class="product-header">🧠 Gerador de Briefing Negocial</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.5])
    with col1:
        emp = st.text_input("Sua Organização:")
        setor = st.text_input("Setor:")
        sel_tags = st.multiselect("Tags do Radar:", options=st.session_state.tags_disponiveis, default=["Novas Leis"])
        nova = st.text_input("➕ Adicionar nova tag:")
        if nova and nova not in st.session_state.tags_disponiveis:
            st.session_state.tags_disponiveis.append(nova)
            st.rerun()
    with col2:
        if st.button("⚡ ESCANEAR MERCADO"):
            with st.spinner("Analisando notícias..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    res = model.generate_content(f"Gere um briefing para {emp} ({setor}) focado em {sel_tags}.")
                    st.markdown(res.text)
                except Exception as e: st.error(f"Erro: {e}")

# --- TELA: ATAS ---
elif menu_selecionado == "Analista de Atas de Governança":
    st.markdown('<div class="product-header">📝 Analista de Atas de Governança</div>', unsafe_allow_html=True)
    notas = st.text_area("Notas da Reunião:", height=250)
    if st.button("📝 GERAR ATA FORMAL"):
        with st.spinner("IA formalizando documento..."):
            try:
                model = genai.GenerativeModel("models/gemini-3-flash-preview")
                res = model.generate_content(f"Transforme em ata formal: {notas}")
                st.markdown(res.text)
                st.download_button("📥 Baixar Documento", res.text, file_name="ata.md")
            except Exception as e: st.error(f"Erro: {e}")

# --- RODAPÉ ---
st.markdown("---")
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Estabilidade Mobile v1.8")