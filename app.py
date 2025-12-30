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

# --- 2. CSS PREMIUM GLASSMORPHISM (BLINDAGEM TOTAL DARK) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');

    /* 1. FUNDO ESCURO GLOBAL ABSOLUTO */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
    .stApp, [data-testid="stMain"], [data-testid="stVerticalBlock"],
    [data-testid="stMarkdownContainer"], .main, [data-testid="stBlock"],
    div[role="dialog"], div[data-baseweb="popover"], [data-testid="stExpander"] {
        background-color: #05070a !important;
        font-family: 'Inter', sans-serif !important;
        color: #ffffff !important;
    }

    /* 2. REMOÇÃO DE ELEMENTOS NATIVOS */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* 3. FORÇA FONTES BRANCAS E LEGÍVEIS EM TUDO (MESMO DENTRO DE BARRAS) */
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
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    }

    /* 5. CORREÇÃO DA BARRA DE SERVIÇOS (SELECTBOX) - REMOVE O BRANCO E GARANTE LEITURA */
    div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(59, 130, 246, 0.5) !important;
        border-radius: 14px !important;
    }
    
    /* Fundo da lista flutuante aberta */
    div[data-baseweb="popover"] > div, ul[role="listbox"], [data-baseweb="listbox"] {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Cor do texto dentro da barra fechada */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        color: #ffffff !important;
    }

    /* 6. BOTÃO "BROWSE FILES" E UPLOADER */
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stFileUploader"] section {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 2px dashed rgba(59, 130, 246, 0.5) !important;
        border-radius: 15px !important;
    }

    /* 7. BOTÃO EXECUTIVO PRINCIPAL (VERDE GLOSSY) */
    .stButton > button { 
        width: 100%; border-radius: 14px; height: 4.5em; font-weight: 700; 
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: none !important;
        outline: none !important;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.2) !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        transition: 0.4s all ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 25px -5px rgba(16, 185, 129, 0.4) !important;
        filter: brightness(1.1);
    }

    /* 8. INPUTS MODERNOS (TEXTO BRANCO GARANTIDO) */
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        padding: 18px !important;
    }
    
    /* 9. SLIDER DE FORMALIDADE */
    .stSlider label, .stSlider span { color: #ffffff !important; }

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
st.markdown('<div style="text-align: center; font-weight: 700; color: #94a3b8; margin-top: 20px; font-size: 12px; letter-spacing: 4px; text-transform: uppercase;">Command Center v7.2</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="main-title">TechnoBolt IA</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #64748b !important; font-size: 20px; margin-bottom: 40px;'>Inteligência Corporativa de Próxima Geração.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📄 Documentos\nResumos executivos focados em traduzir complexidade técnica para Riscos, Custos e Ações.")
    with col2:
        st.markdown("### ✉️ Comunicação\nRedação de e-mails executivos de alto impacto com ajuste fino de tom.")
    with col3:
        st.markdown("### 📊 Inteligência\nMonitoramento competitivo de rivais e análise de sentimento para prevenção de Churn.")
    
    st.markdown("---")
    st.markdown("""
    ### 🛠️ Guia de Operação Corporativa:
    1. **Navegação:** Utilize o menu no topo para alternar entre os 6 módulos.
    2. **Analisador:** Suba arquivos **PDF, DOCX ou TXT**. Processamento McKinsey-style.
    3. **Briefing:** Informe empresa e setor para radar de mercado 2025.
    4. **Atas:** Formalize reuniões a partir de notas brutas.
    """)

elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos</h1><p>Suporte para PDF, DOCX (Word) e TXT</p></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Suba o relatório técnico ou contrato:", type=["pdf", "docx", "txt"])
    
    if arquivo:
        if st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
            with st.spinner("IA processando inteligência técnica..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    if arquivo.type == "application/pdf":
                        c_ia = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        texto_w = extrair_texto_docx(arquivo)
                        c_ia = [f"Analise o seguinte conteúdo de um Word:\n\n{texto_w}"]
                    else:
                        c_ia = [arquivo.read().decode("utf-8")]

                    prompt_doc = """
                    Você é um Consultor de Estratégia Sênior (ex-McKinsey). Analise o documento e produza:
                    - **RESUMO EXECUTIVO** conciso.
                    - **ANÁLISE DE IMPACTO** (RISCO, CUSTO e OPORTUNIDADES).
                    - **PONTOS CRÍTICOS** inegociáveis.
                    - **PLANO DE AÇÃO** imediato.
                    """
                    response = model.generate_content([prompt_doc] + c_ia)
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e: st.error(f"Erro: {e}")

elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1><p>Redação executiva estratégica</p></div>', unsafe_allow_html=True)
    c_e1, c_e2 = st.columns(2)
    with c_e1: cargo = st.text_input("Seu Cargo:", placeholder="Ex: Diretor de Operações")
    with c_e2: dest = st.text_input("Destinatário:", placeholder="Ex: CEO da Holding")
    obj = st.text_area("Objetivo da Mensagem:", placeholder="Ex: Justificar aumento de orçamento...")
    
    # RESTAURAÇÃO DA LINHA DE FORMALIDADE
    formalidade = st.select_slider("Grau de Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    
    if st.button("🚀 GERAR COMUNICAÇÃO PROFISSIONAL"):
        with st.spinner("IA redigindo conteúdo..."):
            model = genai.GenerativeModel(MODEL_NAME)
            prompt_email = f"Como {cargo}, escreva para {dest} sobre {obj}. Use tom {formalidade}. Seja conciso."
            res = model.generate_content(prompt_email)
            st.text_area("Rascunho:", res.text, height=450)

elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Estratégico</h1></div>', unsafe_allow_html=True)
    empresa = st.text_input("Empresa:")
    setor = st.text_input("Setor:")
    tags_s = st.multiselect("Radar:", options=st.session_state.tags, default=["Novas Leis"])
    if st.button("⚡ ESCANEAR MERCADO"):
        model = genai.GenerativeModel(MODEL_NAME)
        res = model.generate_content(f"Briefing executivo para {empresa} no setor {setor} sobre {tags_s}.")
        st.markdown(res.text)

elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas</h1></div>', unsafe_allow_html=True)
    notas = st.text_area("Insira as notas brutas:", height=300)
    if st.button("📝 FORMALIZAR ATA"):
        model = genai.GenerativeModel(MODEL_NAME)
        res = model.generate_content(f"Transforme em ata formal: {notas}")
        st.markdown(res.text)

elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência & Churn</h1></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Radar Rival", "⚠️ Churn"])
    with t1:
        rival = st.text_input("Rival:")
        if st.button("📡 ANALISAR"):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Analise a estratégia da {rival}.")
            st.markdown(res.text)
    with t2:
        feed = st.text_area("Feedback:")
        if st.button("🧠 PREVER RISCO"):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Risco de churn para: {feed}")
            st.markdown(res.text)

st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Edição Final v7.2")