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

# --- 2. CSS ULTRA-PREMIUM (DARK MODE ABSOLUTO E CORREÇÕES VISUAIS) ---
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
    }

    /* REMOÇÃO DE ELEMENTOS NATIVOS */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* FORÇA FONTES BRANCAS EM TUDO */
    * { 
        color: #f8fafc !important; 
        -webkit-text-fill-color: #f8fafc !important;
    }

    /* BARRA DE SELEÇÃO (SELECTBOX) - REMOVE O BRANCO */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="select"], 
    div[data-baseweb="popover"], 
    ul[role="listbox"],
    div[data-baseweb="popover"] * {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        color: #ffffff !important;
    }
    
    /* Hover na lista suspensa */
    li[role="option"]:hover {
        background-color: #1d4ed8 !important;
    }

    /* BOTÕES - VERDE VIBRANTE SEM PRETO OU SOMBRAS DEFORMADAS */
    .stButton > button { 
        width: 100%; border-radius: 14px; height: 4.5em; font-weight: 700; 
        background-color: #10b981 !important; 
        color: #ffffff !important; 
        border: none !important;
        outline: none !important;
        box-shadow: none !important; 
        text-transform: uppercase;
        letter-spacing: 1.5px;
        transition: 0.3s all ease;
    }
    
    .stButton > button:hover, .stButton > button:focus, .stButton > button:active {
        background-color: #059669 !important;
        color: #ffffff !important;
        border: none !important;
        outline: none !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.4) !important;
    }

    /* BOTÃO "BROWSE FILES" - AZUL CORPORATIVO */
    [data-testid="stFileUploader"] button {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
    }

    /* INPUTS E TEXTAREAS - CINZA ESCURO */
    .stTextInput input, .stTextArea textarea {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* HEADER COM GRADIENTE */
    .main-title { 
        font-size: 42px; font-weight: 900; text-align: center; 
        background: linear-gradient(to right, #60a5fa, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent !important;
    }
    
    .product-header { 
        background: rgba(30, 41, 59, 0.4); 
        backdrop-filter: blur(12px);
        padding: 40px; border-radius: 24px; margin-bottom: 35px; 
        text-align: center; border: 1px solid rgba(255, 255, 255, 0.1);
    }

    hr { border: 0.5px solid rgba(255, 255, 255, 0.1) !important; margin: 30px 0; }
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
st.markdown('<div style="text-align: center; font-weight: 700; color: #94a3b8; margin-top: 15px; font-size: 12px; letter-spacing: 3px; text-transform: uppercase;">Command Center v8.0</div>', unsafe_allow_html=True)

menu_opcoes = [
    "🏠 Dashboard Inicial", 
    "📁 Analisador de Documentos & Contratos",
    "✉️ Gerador de Email Inteligente", 
    "🧠 Briefing Negocial Estratégico", 
    "📝 Analista de Atas de Governança",
    "📈 Inteligência Competitiva & Churn"
]
menu_selecionado = st.selectbox("Menu", menu_opcoes, label_visibility="collapsed")
st.markdown("<hr>", unsafe_allow_html=True)

# --- 5. GESTÃO DE ESTADO (TAGS) ---
if 'tags' not in st.session_state:
    st.session_state.tags = ["Novas Leis", "Concorrência", "Inovação Tech", "Cenário Macro", "ESG"]

# --- 6. TELAS DO HUB ---

if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #94a3b8 !important; font-size: 18px;'>Hub Unificado de Inteligência Corporativa Sênior.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📄 Documentos\nResumos executivos focados em traduzir complexidade técnica para tomada de decisão.")
    with col2:
        st.markdown("### ✉️ Comunicação\nRedação de e-mails executivos estratégicos com ajuste de tom e cargo.")
    with col3:
        st.markdown("### 📊 Inteligência\nMonitoramento de mercado e análise de sentimento para retenção de clientes.")
    
    st.markdown("---")
    st.markdown("### 🛠️ Guia de Operação:\n1. Use o menu no topo para navegar.\n2. No Analisador, suba arquivos PDF ou DOCX.\n3. Na Ata, cole notas de reunião para formalização.")

elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos</h1></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Upload (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
    
    if arquivo:
        if st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
            with st.spinner("IA processando inteligência técnica..."):
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
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e: st.error(f"Erro: {e}")

elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: cargo = st.text_input("Seu Cargo:", placeholder="Ex: VP de Operações")
    with c2: dest = st.text_input("Para:", placeholder="Ex: Diretoria Executiva")
    obj = st.text_area("Objetivo da Mensagem:", placeholder="Ex: Solicitar aprovação de budget...")
    formalidade = st.select_slider("Grau de Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    
    if st.button("🚀 GERAR COMUNICAÇÃO PROFISSIONAL"):
        with st.spinner("Redigindo..."):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Como {cargo}, escreva para {dest} sobre {obj}. Tom {formalidade}.")
            st.text_area("Rascunho:", res.text, height=450)

elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Estratégico</h1></div>', unsafe_allow_html=True)
    empresa = st.text_input("Empresa Alvo:")
    if st.button("⚡ ESCANEAR MERCADO"):
        with st.spinner("Analisando notícias globais..."):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Gere um briefing estratégico 2025 para a empresa {empresa}.")
            st.markdown(res.text)

elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas</h1></div>', unsafe_allow_html=True)
    notas = st.text_area("Notas da reunião:", height=300)
    if st.button("📝 FORMALIZAR DOCUMENTO"):
        with st.spinner("IA estruturando documento oficial..."):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Aja como Secretário de Governança. Transforme em ata formal: {notas}")
            st.markdown(res.text)

elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência & Churn</h1></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Radar Rival", "⚠️ Churn"])
    with t1:
        rival = st.text_input("Nome do Concorrente:")
        if st.button("📡 ANALISAR MOVIMENTAÇÕES"):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Analise a estratégia da empresa {rival}.")
            st.markdown(res.text)
    with t2:
        feed = st.text_area("Feedback do cliente:")
        if st.button("🧠 PREVER RISCO"):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Qual o risco de churn para este feedback: {feed}")
            st.markdown(res.text)

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Enterprise Master Edition v8.0")