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

# --- 2. CSS PARA MENU SUPERIOR E ESTILIZAÇÃO CORPORATIVA ---
st.markdown("""
<style>
    /* OCULTA ELEMENTOS QUE CAUSAM PROBLEMAS NO MOBILE */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* ESTILO GERAL */
    .stApp { background-color: #ffffff; color: #1e1e1e; }
    
    /* TITULOS */
    .main-title { 
        font-size: 32px; 
        font-weight: 800; 
        color: #0D1B2A; 
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 16px;
        color: #415A77;
        text-align: center;
        margin-bottom: 25px;
    }

    /* CABEÇALHO DAS FERRAMENTAS */
    .product-header { 
        background: linear-gradient(90deg, #0077b6, #00b4d8); 
        color: white; 
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 25px;
        text-align: center;
    }

    /* BOTÕES EXECUTIVOS */
    .stButton > button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3.5em; 
        font-weight: bold; 
        background-color: #0077b6; 
        color: white; 
        border: none;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #00b4d8;
    }

    /* ESTILO DO SELETOR DE MENU NO TOPO */
    .stSelectbox div[data-baseweb="select"] {
        border: 2px solid #0077b6 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DA API ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 4. SISTEMA DE NAVEGAÇÃO SUPERIOR ---
# No mobile, o Streamlit transforma o selectbox em um menu nativo de fácil toque
st.markdown('<div style="text-align: center; font-weight: bold; color: #0077b6; margin-top: 10px;">SELECIONE A FERRAMENTA:</div>', unsafe_allow_html=True)
menu_opcoes = [
    "🏠 Página Inicial", 
    "✉️ Gerador de Email Inteligente", 
    "🧠 Gerador de Briefing Negocial", 
    "📝 Analista de Atas de Governança"
]
menu_selecionado = st.selectbox("Navegação", menu_opcoes, label_visibility="collapsed")

st.markdown("---")

# --- 5. MEMÓRIA DE SESSÃO (TAGS DO RADAR) ---
if 'tags_disponiveis' not in st.session_state:
    st.session_state.tags_disponiveis = ["Novas Leis", "Concorrência", "Tecnologia", "Macroeconomia", "Tributação"]

# --- 6. FLUXO DE TELAS ---

# --- TELA: HOME ---
if "🏠 Página Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Hub estratégico de produtividade corporativa potencializado por IA.</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🚀 Soluções Corporativas
    Use o menu no topo para navegar entre as soluções:
    
    * **✉️ Gerador de Email Inteligente:** Redija comunicações impecáveis baseadas no seu cargo.
    * **🧠 Gerador de Briefing Negocial:** Radar estratégico via tags personalizadas e notícias reais.
    * **📝 Analista de Atas de Governança:** Formalização instantânea de reuniões de diretoria.
    
    ---
    *Tudo aqui faz uso de Inteligência Artificial de última geração para acelerar seus processos.*
    """)

# --- TELA: GERADOR DE EMAIL ---
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header">✉️ Gerador de Email Inteligente</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1, 1.2])
    with col_a:
        cargo = st.text_input("Qual cargo a IA deve assumir?", placeholder="Ex: Diretor Financeiro")
        destinatario = st.text_input("Para quem você escreve?", placeholder="Ex: Conselho Fiscal")
        objetivo = st.text_area("O que deseja com esse e-mail?", placeholder="Ex: Justificar custos extras...")
    
    with col_b:
        if st.button("🚀 CRIAR E-MAIL COM IA"):
            if not api_key: st.error("API Key não configurada.")
            else:
                with st.spinner("IA redigindo comunicação executiva..."):
                    try:
                        model = genai.GenerativeModel("models/gemini-3-flash-preview")
                        prompt = f"Como {cargo}, escreva para {destinatario} sobre {objetivo}. Use tom profissional."
                        response = model.generate_content(prompt)
                        st.text_area("Resultado:", response.text, height=400)
                    except Exception as e: st.error(f"Erro: {e}")

# --- TELA: BRIEFING ---
elif "🧠 Gerador de Briefing" in menu_selecionado:
    st.markdown('<div class="product-header">🧠 Gerador de Briefing Negocial</div>', unsafe_allow_html=True)
    
    col_c, col_d = st.columns([1, 1.5])
    with col_c:
        empresa = st.text_input("Sua Organização:")
        setor = st.text_input("Setor de Atuação:")
        sel_tags = st.multiselect("Tags do Radar:", options=st.session_state.tags_disponiveis, default=["Novas Leis"])
        nova = st.text_input("➕ Adicionar nova tag personalizada:")
        if nova and nova not in st.session_state.tags_disponiveis:
            st.session_state.tags_disponiveis.append(nova)
            st.rerun()
    
    with col_d:
        if st.button("⚡ ESCANEAR MERCADO"):
            if not empresa or not setor: st.warning("Informe empresa e setor.")
            else:
                with st.spinner("Processando notícias e mercado..."):
                    try:
                        model = genai.GenerativeModel("models/gemini-3-flash-preview")
                        prompt_b = f"Gere um briefing para {empresa} no setor {setor}. Tags: {', '.join(sel_tags)}. Data: {time.strftime('%d/%m/%Y')}."
                        response = model.generate_content(prompt_b)
                        st.markdown(response.text)
                    except Exception as e: st.error(f"Erro: {e}")

# --- TELA: ATAS ---
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header">📝 Analista de Atas de Governança</div>', unsafe_allow_html=True)
    
    notas = st.text_area("Notas e deliberações da reunião:", height=250, placeholder="Ex: O Diretor X aprovou o budget...")
    
    if st.button("📝 FORMALIZAR ATA OFICIAL"):
        if not notas: st.warning("Insira as notas da reunião.")
        else:
            with st.spinner("IA formatando documento formal..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    response = model.generate_content(f"Transforme em ata de diretoria formal: {notas}")
                    st.markdown(response.text)
                    st.download_button("📥 Baixar Documento", response.text, file_name="ata.md")
                except Exception as e: st.error(f"Erro: {e}")

# --- RODAPÉ ---
st.markdown("---")
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Layout Universal v2.1")