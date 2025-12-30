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

# --- 2. CSS DE BLINDAGEM VISUAL (DARK MODE TOTAL) ---
st.markdown("""
<style>
    /* 1. FUNDO ESCURO GLOBAL ABSOLUTO */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
    .stApp, [data-testid="stMain"], [data-testid="stVerticalBlock"],
    [data-testid="stMarkdownContainer"], .main, [data-testid="stBlock"],
    div[role="dialog"], div[data-baseweb="popover"], [data-testid="stExpander"] {
        background-color: #0d1117 !important;
        color: #ffffff !important;
    }

    /* 2. REMOÇÃO DE ELEMENTOS NATIVOS */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* 3. FORÇA FONTES BRANCAS EM TUDO (MESMO DENTRO DE INPUTS E LISTAS) */
    * { 
        color: #ffffff !important; 
        -webkit-text-fill-color: #ffffff !important;
    }

    /* 4. TÍTULO E CABEÇALHOS */
    .main-title { 
        font-size: 42px; font-weight: 900; text-align: center; 
        margin-top: 10px; margin-bottom: 5px; color: #ffffff !important;
        letter-spacing: -1.5px;
    }
    .product-header { 
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%); 
        padding: 35px; border-radius: 20px; margin-bottom: 35px; 
        text-align: center; border: 1px solid #374151;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }

    /* 5. CORREÇÃO DA BARRA DE SERVIÇOS (SELECTBOX) - REMOVE O BRANCO */
    div[data-baseweb="select"] {
        background-color: #161b22 !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 12px !important;
    }
    
    /* Fundo da lista flutuante aberta */
    div[data-baseweb="popover"] > div, ul[role="listbox"], [data-baseweb="listbox"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
    }
    
    /* Itens da lista suspensa */
    li[role="option"] {
        background-color: transparent !important;
        color: #ffffff !important;
        padding: 12px !important;
        transition: 0.3s;
    }
    
    li[role="option"]:hover {
        background-color: #1d4ed8 !important;
    }

    /* 6. CORREÇÃO DO BOTÃO "BROWSE FILES" (UPLOADER) - REMOVE O BRANCO */
    [data-testid="stFileUploader"] button {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stFileUploader"] section {
        background-color: #161b22 !important;
        border: 2px dashed #3b82f6 !important;
        border-radius: 15px !important;
    }

    /* 7. BOTÃO EXECUTIVO (VERDE VIBRANTE SEM DEFORMAÇÃO OU FAIXAS) */
    .stButton > button { 
        width: 100%; border-radius: 15px; height: 4.5em; font-weight: bold; 
        background-color: #238636 !important;
        color: #ffffff !important; 
        border: none !important;
        outline: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover, .stButton > button:focus, .stButton > button:active {
        background-color: #2ea043 !important;
        border: none !important;
        outline: none !important;
        box-shadow: 0 8px 15px rgba(35, 134, 54, 0.4) !important;
    }

    /* 8. INPUTS E TEXTAREAS (TEXTO SEMPRE CLARO) */
    .stTextInput input, .stTextArea textarea {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* TABS E SLIDERS */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: 700; }
    
    hr { border: 0.5px solid #334155 !important; margin: 30px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE: CONFIGURAÇÃO DA API ---
api_key = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "models/gemini-3-flash-preview"

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ GEMINI_API_KEY não encontrada.")

def extrair_texto_docx(arquivo_docx):
    """Extração de texto para suporte total a arquivos Word."""
    doc = docx.Document(arquivo_docx)
    return "\n".join([para.text for para in doc.paragraphs])

# --- 4. NAVEGAÇÃO SUPERIOR ---
st.markdown('<div style="text-align: center; font-weight: bold; color: #60a5fa; margin-top: 15px; font-size: 14px; letter-spacing: 3px; text-transform: uppercase;">TECHNOBOLT AI COMMAND CENTER</div>', unsafe_allow_html=True)

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
    st.markdown("<p style='text-align:center; color: #9ca3af !important; font-size: 18px;'>Plataforma Unificada de Inteligência Corporativa para Alta Gestão.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📄 Documentos\nResumos técnicos traduzidos para visão estratégica de Riscos, Custos e Ações.")
    with col2:
        st.markdown("### ✉️ Comunicação\nRedação executiva de alto impacto com ajuste de cargo e tom.")
    with col3:
        st.markdown("### 📊 Inteligência\nMonitoramento de rivais e análise de Churn através de sentimentos.")
    
    st.markdown("---")
    st.markdown("""
    ### 🛠️ Orientações:
    1. Utilize o menu no topo para navegar entre os módulos.
    2. No Analisador, você pode subir arquivos **PDF, DOCX ou TXT**.
    3. Use o Briefing para escaneamentos rápidos de mercado 2025.
    """)

elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos & Tradutor de Gestão</h1></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Suba o documento (PDF, DOCX ou TXT):", type=["pdf", "docx", "txt"])
    
    if arquivo:
        if st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
            with st.spinner("IA analisando..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    if arquivo.type == "application/pdf":
                        conteudo_ia = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        texto_w = extrair_texto_docx(arquivo)
                        conteudo_ia = [f"Conteúdo extraído Word:\n\n{texto_w}"]
                    else:
                        conteudo_ia = [arquivo.read().decode("utf-8")]

                    prompt = """
                    Atue como um Consultor Sênior. Forneça:
                    - RESUMO EXECUTIVO direto ao ponto.
                    - TRADUÇÃO PARA NEGÓCIO (Risco, Custo, Oportunidade).
                    - PLANO DE AÇÃO sugerido.
                    - RESPOSTA FORMAL para o autor do documento.
                    """
                    response = model.generate_content([prompt] + conteudo_ia)
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e: st.error(f"Erro: {e}")

elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: cargo = st.text_input("Seu Cargo:")
    with c2: dest = st.text_input("Destinatário:")
    obj = st.text_area("Objetivo da Mensagem:")
    formalidade = st.select_slider("Grau de Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    
    if st.button("🚀 GERAR COMUNICAÇÃO PROFISSIONAL"):
        with st.spinner("Redigindo..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_e = f"Como {cargo}, escreva para {dest} sobre {obj}. Tom: {formalidade}."
                res = model.generate_content(prompt_e)
                st.text_area("Cópia disponível:", res.text, height=450)
            except Exception as e: st.error(e)

elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Estratégico</h1></div>', unsafe_allow_html=True)
    emp = st.text_input("Empresa:")
    if st.button("⚡ ESCANEAR MERCADO"):
        with st.spinner("IA Cruzando notícias..."):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Gere briefing executivo 2025 para {emp}.")
            st.markdown(res.text)

elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas</h1></div>', unsafe_allow_html=True)
    notas = st.text_area("Notas da reunião:", height=300)
    if st.button("📝 FORMALIZAR DOCUMENTO"):
        with st.spinner("Estruturando ata..."):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Transforme em ata formal de diretoria: {notas}")
            st.markdown(res.text)

elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência & Churn</h1></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Radar Rival", "⚠️ Churn"])
    with t1:
        rival = st.text_input("Concorrente:")
        if st.button("📡 ANALISAR MOVIMENTAÇÕES"):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Analise a empresa {rival}.")
            st.markdown(res.text)
    with t2:
        feed = st.text_area("Feedback do cliente:")
        if st.button("🧠 AVALIAR RISCO"):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Risco de perda para: {feed}")
            st.markdown(res.text)

st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | v6.0 Full Edition")