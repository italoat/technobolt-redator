import streamlit as st
import google.generativeai as genai
import os
import time
import docx  # Requer: pip install python-docx

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="TechnoBolt IA - Hub Corporativo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS PREMIUM OBSIDIAN (DARK MODE & BARRAS CINZA ESCURO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');

    /* FUNDO PRETO GLOBAL ABSOLUTO */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
    .stApp, [data-testid="stMain"], [data-testid="stVerticalBlock"],
    [data-testid="stMarkdownContainer"], .main, [data-testid="stBlock"],
    div[role="dialog"], div[data-baseweb="popover"], [data-testid="stExpander"] {
        background-color: #05070a !important;
        font-family: 'Inter', sans-serif !important;
        color: #ffffff !important;
    }

    /* REMOÇÃO DE ELEMENTOS NATIVOS E CABEÇALHOS */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* FORÇA TODAS AS FONTES PARA BRANCO */
    * { 
        color: #f8fafc !important; 
        -webkit-text-fill-color: #f8fafc !important;
    }

    /* HEADER CORPORATIVO COM GRADIENTE NEON */
    .main-title { 
        font-size: 48px; font-weight: 900; text-align: center; 
        background: linear-gradient(to right, #60a5fa, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent !important;
        letter-spacing: -2px; margin-bottom: 5px;
    }

    .product-header { 
        background: rgba(30, 41, 59, 0.4); 
        backdrop-filter: blur(12px);
        padding: 40px; border-radius: 24px; margin-bottom: 35px; 
        text-align: center; border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    }

    /* BARRAS DE INTERAÇÃO (CINZA ESCURO #161B22) */
    div[data-baseweb="select"] > div { background-color: #161b22 !important; border-radius: 12px !important; }
    div[data-baseweb="select"], div[data-baseweb="popover"], ul[role="listbox"], [data-baseweb="listbox"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
    }
    li[role="option"]:hover { background-color: #1d4ed8 !important; }

    /* INPUTS E TEXTAREAS (CINZA ESCURO) */
    .stTextInput input, .stTextArea textarea {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 18px !important;
    }

    /* BOTÃO "BROWSE FILES" E ÁREA DE UPLOAD */
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 10px 25px !important;
    }
    [data-testid="stFileUploader"] section {
        background-color: #161b22 !important;
        border: 2px dashed #3b82f6 !important;
        border-radius: 15px;
    }

    /* BOTÕES EXECUTIVOS (VERDE VIBRANTE) */
    .stButton > button { 
        width: 100%; border-radius: 14px; height: 4.5em; font-weight: 700; 
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: none !important;
        outline: none !important;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.2) !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        transition: 0.3s all ease;
    }
    .stButton > button:hover { transform: translateY(-2px); filter: brightness(1.1); }

    /* SLIDERS E TABS */
    .stSlider label, .stSlider span { color: #ffffff !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: 700; }

    hr { border: 0.5px solid rgba(255, 255, 255, 0.1) !important; margin: 40px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE: CONFIGURAÇÃO DA API ---
api_key = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "models/gemini-3-flash-preview"
if api_key:
    genai.configure(api_key=api_key)

def extrair_texto_docx(arquivo_docx):
    doc = docx.Document(arquivo_docx)
    return "\n".join([para.text for para in doc.paragraphs])

# --- 4. NAVEGAÇÃO SUPERIOR ---
st.markdown('<div style="text-align: center; font-weight: 700; color: #94a3b8; margin-top: 20px; font-size: 12px; letter-spacing: 4px; text-transform: uppercase;">Command Center v7.6</div>', unsafe_allow_html=True)

menu_opcoes = [
    "🏠 Dashboard Inicial", 
    "📁 Analisador de Documentos & Contratos",
    "✉️ Gerador de Email Inteligente", 
    "🧠 Briefing Negocial Estratégico", 
    "📝 Analista de Atas de Governança",
    "📈 Inteligência Competitiva & Churn"
]
menu_selecionado = st.selectbox("Seletor de Módulo", menu_opcoes, label_visibility="collapsed")
st.markdown("<hr>", unsafe_allow_html=True)

# --- 5. GESTÃO DE ESTADO (TAGS) ---
if 'tags' not in st.session_state:
    st.session_state.tags = ["Novas Leis", "Concorrência", "Inovação Tech", "Cenário Macro", "ESG"]

# --- 6. TELAS DO HUB (LÓGICA INTEGRAL) ---

# TELA 1: DASHBOARD
if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #64748b !important; font-size: 20px; margin-bottom: 40px;'>Inteligência Corporativa de Próxima Geração.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📄 Documentos\nResumos executivos focados em traduzir complexidade técnica para tomada de decisão.")
    with col2:
        st.markdown("### ✉️ Comunicação\nRedação de e-mails executivos estratégicos com ajuste de cargo e tom.")
    with col3:
        st.markdown("### 📊 Inteligência\nMonitoramento de mercado e análise de sentimento para retenção de clientes.")
    
    st.markdown("---")
    st.markdown("### 🛠️ Guia de Uso:\n1. Use o menu no topo para navegar.\n2. No Analisador, suba PDF/Word.\n3. Na Ata, cole as notas da reunião para formalização.")

# TELA 2: ANALISADOR
elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos</h1></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Suba o arquivo (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
    if arquivo and st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
        with st.spinner("IA processando inteligência..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                if arquivo.type == "application/pdf":
                    c_ia = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    texto_w = extrair_texto_docx(arquivo)
                    c_ia = [f"Texto Word extraído:\n\n{texto_w}"]
                else:
                    c_ia = [arquivo.read().decode()]
                
                prompt = "Aja como Consultor McKinsey. Gere: Resumo Executivo, Análise de Risco/Custo, Pontos Críticos e Plano de Ação."
                res = model.generate_content([prompt] + c_ia)
                st.markdown(res.text)
            except Exception as e: st.error(f"Erro: {e}")

# TELA 3: EMAIL
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: cargo = st.text_input("Seu Cargo:", placeholder="Ex: Diretor de Operações")
    with col2: dest = st.text_input("Destinatário:", placeholder="Ex: CEO")
    obj = st.text_area("Objetivo da Mensagem:", placeholder="Ex: Solicitar aprovação de budget...")
    formalidade = st.select_slider("Grau de Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    if st.button("🚀 GERAR COMUNICAÇÃO PROFISSIONAL"):
        with st.spinner("Redigindo..."):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Como {cargo}, escreva para {dest} sobre {obj}. Tom: {formalidade}.")
            st.text_area("Rascunho:", res.text, height=450)

# TELA 4: BRIEFING
elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Estratégico</h1></div>', unsafe_allow_html=True)
    empresa = st.text_input("Empresa Alvo:")
    tags_s = st.multiselect("Radar:", options=st.session_state.tags, default=["Novas Leis"])
    if st.button("⚡ ESCANEAR MERCADO"):
        with st.spinner("Analisando mercado..."):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Briefing executivo para {empresa} focado em {tags_s}.")
            st.markdown(res.text)

# TELA 5: ATAS
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas de Governança</h1></div>', unsafe_allow_html=True)
    notas_brutas = st.text_area("Insira as notas brutas da reunião:", height=300)
    if st.button("📝 GERAR ATA OFICIAL"):
        if notas_brutas:
            with st.spinner("Estruturando documento..."):
                model = genai.GenerativeModel(MODEL_NAME)
                res = model.generate_content(f"Transforme estas notas em uma ata formal de diretoria estruturada: {notas_brutas}")
                st.markdown("---")
                st.markdown(res.text)
        else: st.warning("Insira as notas antes de gerar.")

# TELA 6: INTELIGÊNCIA COMPETITIVA
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência & Churn</h1></div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔍 Radar Rival", "⚠️ Previsão Churn"])
    with tab1:
        rival = st.text_input("Nome do Rival:")
        if st.button("📡 ANALISAR MOVIMENTAÇÕES"):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Analise a estratégia recente da {rival}.")
            st.markdown(res.text)
    with tab2:
        feed = st.text_area("Feedback do cliente:")
        if st.button("🧠 AVALIAR RISCO"):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Risco de churn para: {feed}")
            st.markdown(res.text)

st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Enterprise Strategic v7.6 Full")