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

# --- 2. CSS PARA DARK MODE TOTAL, FONTES BRANCAS E UI EXECUTIVA ---
st.markdown("""
<style>
    /* OCULTA ELEMENTOS PADRÃO DO STREAMLIT */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* FUNDO ESCURO PROFUNDO (ESTILO GITHUB DARK) */
    .stApp { 
        background-color: #0d1117 !important; 
        color: #ffffff !important; 
    }

    /* FORÇA TODAS AS FONTES PARA BRANCO PURO */
    h1, h2, h3, h4, h5, h6, p, label, span, div, .stMarkdown, [data-testid="stWidgetLabel"] p { 
        color: #ffffff !important; 
    }

    /* TÍTULO PRINCIPAL */
    .main-title { 
        font-size: 36px; 
        font-weight: 800; 
        color: #ffffff !important; 
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }

    /* CABEÇALHO DAS FERRAMENTAS */
    .product-header { 
        background: linear-gradient(90deg, #161b22, #0d1117); 
        color: #ffffff !important; 
        padding: 22px; 
        border-radius: 12px; 
        margin-bottom: 30px;
        text-align: center;
        border: 1px solid #30363d;
    }

    /* MENU SUPERIOR (SELECTBOX) DARK MODE */
    div[data-baseweb="select"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    
    div[data-baseweb="select"] * {
        color: #ffffff !important;
        background-color: transparent !important;
    }

    /* INPUTS E TEXTAREAS */
    .stTextInput input, .stTextArea textarea {
        background-color: #0d1117 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }

    /* BOTÃO GERAR (VERDE CORPORATIVO) */
    .stButton > button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3.8em; 
        font-weight: bold; 
        background-color: #238636 !important; 
        color: #ffffff !important; 
        border: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #2ea043 !important;
        transform: translateY(-2px);
    }
    
    /* TAGS E TABS */
    span[data-baseweb="tag"] {
        background-color: #388bfd !important;
        color: #ffffff !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
    }

    /* LINHA DIVISORA */
    hr { border: 0.5px solid #30363d !important; }

</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DA API ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 4. SISTEMA DE NAVEGAÇÃO SUPERIOR ---
st.markdown('<div style="text-align: center; font-weight: bold; color: #58a6ff; margin-top: 15px; font-size: 13px;">CENTRAL DE COMANDO</div>', unsafe_allow_html=True)
menu_opcoes = [
    "🏠 Página Inicial", 
    "✉️ Gerador de Email Inteligente", 
    "🧠 Gerador de Briefing Negocial", 
    "📝 Analista de Atas de Governança",
    "📈 Inteligência Competitiva"
]
menu_selecionado = st.selectbox("Menu", menu_opcoes, label_visibility="collapsed")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 5. MEMÓRIA DE SESSÃO (TAGS) ---
if 'tags_disponiveis' not in st.session_state:
    st.session_state.tags_disponiveis = ["Novas Leis", "Concorrência", "Tecnologia", "Mercado Financeiro", "Churn"]

# --- 6. TELAS DO HUB ---

# --- HOME ---
if "🏠 Página Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #8b949e !important;'>Hub estratégico de produtividade e inteligência para alta gestão.</p>", unsafe_allow_html=True)
    
    st.markdown("""
    ### 🚀 Soluções Corporativas Disponíveis:
    * **✉️ Gerador de Email:** Redação executiva com ajuste de cargo e formalidade.
    * **🧠 Briefing Negocial:** Radar estratégico em tempo real via tags livres.
    * **📝 Analista de Atas:** Formalização instantânea de decisões de diretoria.
    * **📈 Inteligência Competitiva:** Análise de rivais e monitoramento de saúde de clientes.
    """)

# --- GERADOR DE EMAIL ---
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header">✉️ Gerador de Email Inteligente</div>', unsafe_allow_html=True)
    cargo = st.text_input("Cargo que a IA deve assumir:", placeholder="Ex: Diretor de Vendas")
    dest = st.text_input("Destinatário:", placeholder="Ex: CEO da Empresa Alpha")
    obj = st.text_area("Objetivo da comunicação:", placeholder="Ex: Solicitar renegociação de prazos...")
    formalidade = st.select_slider("Grau de Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    
    if st.button("🚀 GERAR E-MAIL PROFISSIONAL"):
        with st.spinner("IA redigindo..."):
            try:
                model = genai.GenerativeModel("models/gemini-3-flash-preview")
                prompt = f"Como {cargo}, escreva para {dest} sobre {obj}. Tom: {formalidade}."
                response = model.generate_content(prompt)
                st.text_area("Resultado:", response.text, height=400)
            except Exception as e: st.error(f"Erro: {e}")

# --- BRIEFING NEGOCIAL ---
elif "🧠 Gerador de Briefing" in menu_selecionado:
    st.markdown('<div class="product-header">🧠 Gerador de Briefing Negocial</div>', unsafe_allow_html=True)
    empresa = st.text_input("Nome da sua Empresa:")
    setor = st.text_input("Setor de Atuação:")
    tags_sel = st.multiselect("Radar de Prioridades:", options=st.session_state.tags_disponiveis, default=["Novas Leis"])
    if st.button("⚡ ESCANEAR MERCADO"):
        with st.spinner("IA processando radar 2025..."):
            try:
                model = genai.GenerativeModel("models/gemini-3-flash-preview")
                prompt_b = f"Gere briefing executivo para {empresa} ({setor}). Foco: {', '.join(tags_sel)}."
                response = model.generate_content(prompt_b)
                st.markdown(response.text)
            except Exception as e: st.error(f"Erro: {e}")

# --- ANALISTA DE ATAS ---
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header">📝 Analista de Atas de Governança</div>', unsafe_allow_html=True)
    notas = st.text_area("Decisões e tópicos da reunião:", height=250)
    if st.button("📝 FORMALIZAR DOCUMENTO"):
        with st.spinner("Estruturando documento oficial..."):
            try:
                model = genai.GenerativeModel("models/gemini-3-flash-preview")
                response = model.generate_content(f"Transforme em ata de diretoria formal: {notas}")
                st.markdown(response.text)
            except Exception as e: st.error(f"Erro: {e}")

# --- INTELIGÊNCIA COMPETITIVA ---
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header">📈 Inteligência Competitiva e Sentimento</div>', unsafe_allow_html=True)
    aba1, aba2 = st.tabs(["🔍 Radar de Concorrência", "❤️ Sentimento do Cliente"])
    
    with aba1:
        concorrente = st.text_input("Empresa Rival:", placeholder="Nome do concorrente")
        if st.button("📡 ANALISAR RIVAL"):
            with st.spinner("Escaneando mercado..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    res = model.generate_content(f"Analise a estratégia atual da {concorrente} e aponte brechas comerciais.")
                    st.markdown(res.text)
                except Exception as e: st.error(e)
                
    with aba2:
        feedback = st.text_area("Feedback do Cliente:", placeholder="Cole o texto aqui para análise de risco de perda (Churn)")
        if st.button("🧠 PREVER RISCO"):
            with st.spinner("Analisando entrelinhas..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    res = model.generate_content(f"Analise o risco de cancelamento baseado neste feedback: {feedback}")
                    st.markdown(res.text)
                except Exception as e: st.error(e)

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Corporativo v2.6 stable")