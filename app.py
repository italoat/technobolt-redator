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

# --- 2. CSS ULTRA-PREMIUM (DARK MODE ABSOLUTO E BLINDAGEM VISUAL) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');

    /* 1. FUNDO PRETO GLOBAL ABSOLUTO */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
    .stApp, [data-testid="stMain"], [data-testid="stVerticalBlock"],
    [data-testid="stMarkdownContainer"], .main, [data-testid="stBlock"] {
        background-color: #05070a !important;
        font-family: 'Inter', sans-serif !important;
        color: #ffffff !important;
    }

    /* 2. REMOÇÃO DE ELEMENTOS NATIVOS */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* 3. FORÇA FONTES BRANCAS EM TUDO */
    * { 
        color: #f8fafc !important; 
        -webkit-text-fill-color: #f8fafc !important;
    }

    /* 4. TÍTULO CORPORATIVO COM GRADIENTE */
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
    }

    /* 5. CORREÇÃO "NUCLEAR" DA BARRA DE SERVIÇOS (SELECTBOX) E POPOVER */
    /* Fundo da barra fechada */
    div[data-baseweb="select"] > div {
        background-color: #161b22 !important;
        border-radius: 12px !important;
    }

    /* Fundo da barra e da lista flutuante aberta */
    div[data-baseweb="select"], 
    div[data-baseweb="popover"], 
    div[data-baseweb="popover"] > div,
    ul[role="listbox"], 
    [data-baseweb="listbox"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
    }
    
    /* Itens individuais da lista suspensa */
    li[role="option"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        transition: 0.2s;
    }
    
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }

    /* 6. INPUTS E TEXTAREAS (CINZA ESCURO) */
    .stTextInput input, .stTextArea textarea {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* 7. BOTÃO "BROWSE FILES" E ÁREA DE UPLOAD */
    [data-testid="stFileUploader"] section {
        background-color: #161b22 !important;
        border: 2px dashed #3b82f6 !important;
        border-radius: 15px !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 10px 25px !important;
    }

    /* 8. BOTÕES EXECUTIVOS (CORREÇÃO DE FAIXA PRETA E SOMBRA) */
    .stButton > button { 
        width: 100%; border-radius: 14px; height: 4.5em; font-weight: 700; 
        background-color: #10b981 !important; /* Verde sólido para evitar bugs de gradiente */
        color: #ffffff !important; 
        border: none !important;
        outline: none !important;
        box-shadow: none !important; 
        text-shadow: none !important; /* REMOVE SOMBRA INTERNA DO TEXTO */
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .stButton > button:hover, .stButton > button:focus, .stButton > button:active {
        background-color: #2ea043 !important;
        color: #ffffff !important;
        border: none !important;
        outline: none !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
        transform: translateY(-2px);
    }

    /* 9. SLIDER E TABS */
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
    return "\n".join([p.text for p in doc.paragraphs])

# --- 4. NAVEGAÇÃO SUPERIOR ---
st.markdown('<div style="text-align: center; font-weight: 700; color: #94a3b8; margin-top: 15px; font-size: 12px; letter-spacing: 3px; text-transform: uppercase;">Command Center v9.0</div>', unsafe_allow_html=True)

menu_opcoes = [
    "🏠 Dashboard Inicial", 
    "📁 Analisador de Documentos & Contratos",
    "📧 Email Intel: Auditoria em Lote",
    "✉️ Gerador de Email Inteligente", 
    "🧠 Briefing Negocial Estratégico", 
    "📝 Analista de Atas de Governança",
    "📈 Inteligência Competitiva & Churn"
]
menu_selecionado = st.selectbox("Menu", menu_opcoes, label_visibility="collapsed")
st.markdown("<hr>", unsafe_allow_html=True)

# --- 5. GESTÃO DE ESTADO ---
if 'tags' not in st.session_state:
    st.session_state.tags = ["Novas Leis", "Concorrência", "Inovação Tech", "Cenário Macro", "ESG"]

# --- 6. TELAS DO HUB ---

# DASHBOARD
if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #94a3b8 !important; font-size: 18px;'>Hub Unificado de Inteligência Corporativa Sênior.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📄 Documentos\nResumos executivos focados em traduzir complexidade técnica para tomada de decisão.")
    with col2:
        st.markdown("### 📧 Email Intel\nAuditoria de múltiplos e-mails em PDF com geração automática de minutas de resposta.")
    with col3:
        st.markdown("### 📊 Inteligência\nMonitoramento de mercado e análise de sentimento para retenção de clientes.")
    
    st.markdown("---")
    st.markdown("### 🛠️ Guia de Operação:\n1. Use o menu no topo para navegar.\n2. No **Analisador**, suba PDF/DOCX para relatórios McKinsey-style.\n3. No **Email Intel**, suba vários PDFs para processamento em lote.")

# ANALISADOR DE DOCUMENTOS
elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos</h1></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Upload (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
    if arquivo and st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
        with st.spinner("Processando inteligência técnica..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                if arquivo.type == "application/pdf":
                    conteudo = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    texto = extrair_texto_docx(arquivo)
                    conteudo = [f"Analise estrategicamente este Word:\n\n{texto}"]
                else:
                    conteudo = [arquivo.read().decode("utf-8")]

                prompt = """
                Atue como Consultor Sênior McKinsey. Analise o documento e gere:
                - **RESUMO EXECUTIVO** direto ao ponto.
                - **ANÁLISE DE IMPACTO** (RISCO, CUSTO, OPORTUNIDADE).
                - **PLANO DE AÇÃO** de 3 passos.
                - **SUGESTÃO DE RESPOSTA** formal.
                """
                response = model.generate_content([prompt] + conteudo)
                st.markdown(response.text)
            except Exception as e: st.error(f"Erro: {e}")

# NOVA SOLUÇÃO: EMAIL INTEL AUDITORIA
elif "📧 Email Intel" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📧 Email Intel: Auditoria & Resposta</h1></div>', unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 2])
    with col_a:
        arquivos = st.file_uploader("Anexe e-mails (PDF):", type=["pdf"], accept_multiple_files=True)
        cargo = st.text_input("Seu Cargo para Resposta:", placeholder="Ex: Diretor Financeiro")
        tom = st.selectbox("Tom da Resposta:", ["Executivo/Direto", "Diplomático", "Firme", "Cordial"])
        disparar = st.button("🔍 AUDITAR EM LOTE")
    with col_b:
        if arquivos and disparar:
            model = genai.GenerativeModel(MODEL_NAME)
            for i, pdf in enumerate(arquivos):
                with st.expander(f"E-mail {i+1}: {pdf.name}", expanded=True):
                    conteudo_pdf = [{"mime_type": "application/pdf", "data": pdf.read()}]
                    prompt_intel = f"Resuma este e-mail, identifique riscos e proponha uma resposta como {cargo} em tom {tom}."
                    res = model.generate_content([prompt_intel] + conteudo_pdf)
                    st.markdown(res.text)

# GERADOR DE EMAIL (INDIVIDUAL)
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: cargo_e = st.text_input("Seu Cargo:", placeholder="Ex: VP de Operações")
    with c2: dest_e = st.text_input("Para:", placeholder="Ex: Diretoria Executiva")
    obj_e = st.text_area("Objetivo da Mensagem:")
    formalidade = st.select_slider("Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    if st.button("🚀 GERAR COMUNICAÇÃO"):
        model = genai.GenerativeModel(MODEL_NAME)
        res = model.generate_content(f"Como {cargo_e}, escreva para {dest_e} sobre {obj_e}. Tom {formalidade}.")
        st.text_area("Rascunho:", res.text, height=400)

# BRIEFING
elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Estratégico</h1></div>', unsafe_allow_html=True)
    empresa = st.text_input("Empresa Alvo:")
    if st.button("⚡ ESCANEAR MERCADO"):
        model = genai.GenerativeModel(MODEL_NAME)
        res = model.generate_content(f"Gere um briefing estratégico 2025 para a empresa {empresa}.")
        st.markdown(res.text)

# ATAS
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas</h1></div>', unsafe_allow_html=True)
    notas = st.text_area("Notas da reunião:", height=300)
    if st.button("📝 FORMALIZAR"):
        model = genai.GenerativeModel(MODEL_NAME)
        res = model.generate_content(f"Aja como Secretário de Governança. Transforme em ata formal: {notas}")
        st.markdown(res.text)

# INTELIGÊNCIA COMPETITIVA
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência & Churn</h1></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Radar Rival", "⚠️ Churn"])
    with t1:
        rival = st.text_input("Nome do Rival:")
        if st.button("📡 ANALISAR"):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Analise a estratégia da empresa {rival}.")
            st.markdown(res.text)
    with t2:
        feed = st.text_area("Feedback do cliente:")
        if st.button("🧠 PREVER RISCO"):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Qual o risco de churn para: {feed}")
            st.markdown(res.text)

st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Master Edition v9.0")