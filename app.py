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

# --- 2. CSS ULTRA FORÇADO PARA DARK MODE E FONTES BRANCAS ---
st.markdown("""
<style>
    /* 1. FORÇA FUNDO ESCURO GLOBAL */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #0d1117 !important;
        color: #ffffff !important;
    }

    /* 2. OCULTA ELEMENTOS PADRÃO DO STREAMLIT */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* 3. FORÇA TODAS AS FONTES PARA BRANCO */
    h1, h2, h3, h4, h5, h6, p, label, span, div, .stMarkdown, 
    [data-testid="stWidgetLabel"] p, [data-testid="stHeader"], 
    [data-testid="stMarkdownContainer"] p { 
        color: #ffffff !important; 
    }

    /* 4. TÍTULO E CABEÇALHOS CUSTOMIZADOS */
    .main-title { 
        font-size: 36px; font-weight: 800; text-align: center; 
        margin-bottom: 5px; color: #ffffff !important;
    }
    .product-header { 
        background: linear-gradient(90deg, #161b22, #0d1117); 
        padding: 22px; border-radius: 12px; margin-bottom: 30px; 
        text-align: center; border: 1px solid #30363d;
    }

    /* 5. CORREÇÃO DO MENU DE NAVEGAÇÃO (SELECTBOX) */
    div[data-baseweb="select"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #161b22 !important;
        color: #ffffff !important;
    }
    
    /* Dropdown das opções */
    ul[role="listbox"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
    }
    li[role="option"] {
        color: #ffffff !important;
        background-color: #161b22 !important;
    }
    li[role="option"]:hover {
        background-color: #30363d !important;
    }

    /* 6. INPUTS, TEXTAREAS E SLIDERS */
    .stTextInput input, .stTextArea textarea {
        background-color: #0d1117 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
    }
    .stSlider label, .stSlider span {
        color: #ffffff !important;
    }

    /* 7. BOTÃO EXECUTIVO (VERDE) */
    .stButton > button { 
        width: 100%; border-radius: 10px; height: 3.8em; font-weight: bold; 
        background-color: #238636 !important; color: #ffffff !important; border: none;
    }
    .stButton > button:hover {
        background-color: #2ea043 !important;
        border: none;
    }

    /* 8. UPLOAD DE ARQUIVO */
    [data-testid="stFileUploader"] section {
        background-color: #161b22 !important;
        border: 1px dashed #30363d !important;
    }
    [data-testid="stFileUploader"] label {
        color: #ffffff !important;
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
    }

    hr { border: 0.5px solid #30363d !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DA API E MODELO ---
api_key = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "models/gemini-3-flash-preview"

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API Key não configurada.")

# --- 4. SISTEMA DE NAVEGAÇÃO SUPERIOR ---
st.markdown('<div style="text-align: center; font-weight: bold; color: #58a6ff; margin-top: 15px; font-size: 13px; letter-spacing: 1px;">CENTRAL DE INTELIGÊNCIA</div>', unsafe_allow_html=True)

menu_opcoes = [
    "🏠 Página Inicial", 
    "📁 Analisador de Documentos",
    "✉️ Gerador de Email Inteligente", 
    "🧠 Gerador de Briefing Negocial", 
    "📝 Analista de Atas de Governança",
    "📈 Inteligência Competitiva"
]

menu_selecionado = st.selectbox("Selecione", menu_opcoes, label_visibility="collapsed")
st.markdown("<hr>", unsafe_allow_html=True)

# --- 5. TELAS ---

if "🏠 Página Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #8b949e !important;'>Otimizado para Alta Gestão Corporativa.</p>", unsafe_allow_html=True)
    st.markdown("""
    ### 🚀 Hub de Inteligência Ativa:
    - **📁 Analisador de Documentos:** Traduz relatórios técnicos para Risco e Custo.
    - **✉️ Gerador de Email:** Comunicação executiva com ajuste de tom.
    - **🧠 Briefing Negocial:** Radar de mercado em tempo real.
    - **📈 Inteligência Competitiva:** Monitoramento de rivais e churn.
    """)

elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header">📁 Analisador de Documentos & Tradutor de Gestão</div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Suba um relatório técnico ou contrato:", type=["pdf", "txt", "docx"])
    
    if arquivo:
        if st.button("🔍 ANALISAR PARA GESTÃO"):
            with st.spinner("IA processando estratégia..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    conteudo = arquivo.read()
                    prompt = """
                    Atue como um Consultor Estratégico Sênior. 
                    Analise o documento e forneça:
                    1. Resumo Executivo simples.
                    2. Tradução para Impacto Financeiro (Custo), Riscos e Oportunidades.
                    3. Plano de Ação (3 passos).
                    4. Uma sugestão de resposta formal para o autor do documento.
                    """
                    response = model.generate_content([prompt, {"mime_type": arquivo.type, "data": conteudo}])
                    st.markdown(response.text)
                except Exception as e: st.error(f"Erro: {e}")

elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header">✉️ Gerador de Email Inteligente</div>', unsafe_allow_html=True)
    cargo = st.text_input("Seu Cargo:")
    dest = st.text_input("Destinatário:")
    obj = st.text_area("Objetivo da mensagem:")
    formalidade = st.select_slider("Grau de Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    if st.button("🚀 GERAR E-MAIL"):
        with st.spinner("IA redigindo..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                res = model.generate_content(f"Como {cargo}, escreva para {dest} sobre {obj}. Tom: {formalidade}.")
                st.text_area("Resultado:", res.text, height=400)
            except Exception as e: st.error(f"Erro: {e}")

elif "🧠 Gerador de Briefing" in menu_selecionado:
    st.markdown('<div class="product-header">🧠 Gerador de Briefing Negocial</div>', unsafe_allow_html=True)
    emp = st.text_input("Empresa:")
    setor = st.text_input("Setor:")
    if st.button("⚡ ESCANEAR MERCADO"):
        with st.spinner("Analisando notícias..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                res = model.generate_content(f"Gere briefing executivo para {emp} no setor {setor}.")
                st.markdown(res.text)
            except Exception as e: st.error(f"Erro: {e}")

elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header">📈 Inteligência Competitiva</div>', unsafe_allow_html=True)
    aba1, aba2 = st.tabs(["🔍 Radar Rival", "❤️ Risco de Churn"])
    with aba1:
        rival = st.text_input("Nome do Concorrente:")
        if st.button("📡 ANALISAR RIVAL"):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                res = model.generate_content(f"Analise estrategicamente a {rival}.")
                st.markdown(res.text)
            except Exception as e: st.error(f"Erro: {e}")
    with aba2:
        fb = st.text_area("Feedback do Cliente:")
        if st.button("🧠 PREVER RISCO"):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                res = model.generate_content(f"Analise o risco de perda baseado neste feedback: {fb}")
                st.markdown(res.text)
            except Exception as e: st.error(f"Erro: {e}")

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Strategic Edition v3.1")