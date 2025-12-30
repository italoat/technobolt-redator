import streamlit as st
import google.generativeai as genai
import os
import time
import docx  # Requer: pip install python-docx

# --- 1. CONFIGURAÇÃO DA PÁGINA (ESTADO INICIAL) ---
st.set_page_config(
    page_title="TechnoBolt IA - Hub Corporativo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS AVANÇADO (DARK MODE TOTAL & RESPONSIVIDADE) ---
st.markdown("""
<style>
    /* FUNDO ESCURO GLOBAL E FONTES BRANCAS */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #0d1117 !important;
        color: #ffffff !important;
    }

    /* REMOÇÃO DE ELEMENTOS NATIVOS */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* ESTILIZAÇÃO DE TEXTOS E LABELS */
    h1, h2, h3, h4, h5, h6, p, label, span, div, .stMarkdown, 
    [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p { 
        color: #ffffff !important; 
    }

    /* TÍTULO E CABEÇALHOS CORPORATIVOS */
    .main-title { 
        font-size: 38px; font-weight: 900; text-align: center; 
        margin-top: 10px; margin-bottom: 5px; color: #ffffff !important;
        letter-spacing: -1.5px;
    }
    .product-header { 
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%); 
        padding: 30px; border-radius: 15px; margin-bottom: 30px; 
        text-align: center; border: 1px solid #374151;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* CUSTOMIZAÇÃO DE INPUTS (SELECTBOX, TEXT, AREA) */
    div[data-baseweb="select"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 10px;
    }
    div[data-baseweb="select"] > div {
        background-color: transparent !important;
        color: #ffffff !important;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #0d1117 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }

    /* BOTÕES EXECUTIVOS (ESTILO PREMIUM) */
    .stButton > button { 
        width: 100%; border-radius: 12px; height: 4em; font-weight: bold; 
        background-color: #238636 !important; color: #ffffff !important; 
        border: none; text-transform: uppercase; letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #2ea043 !important;
        transform: scale(1.01);
        box-shadow: 0 0 15px rgba(35, 134, 54, 0.4);
    }

    /* ÁREA DE UPLOAD */
    [data-testid="stFileUploader"] section {
        background-color: #161b22 !important;
        border: 2px dashed #30363d !important;
        border-radius: 15px;
        padding: 20px;
    }

    /* TABS E TAGS */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: 600; }
    span[data-baseweb="tag"] { background-color: #1d4ed8 !important; color: #ffffff !important; border-radius: 5px; }
    
    hr { border: 0.5px solid #30363d !important; margin: 25px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE: CONFIGURAÇÃO DA API E MODELO ---
api_key = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "models/gemini-3-flash-preview"

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Configuração Pendente: GEMINI_API_KEY não encontrada.")

def extrair_texto_docx(arquivo_docx):
    """Lê arquivos Word e extrai o texto parágrafo por parágrafo."""
    doc = docx.Document(arquivo_docx)
    return "\n".join([para.text for para in doc.paragraphs])

# --- 4. SISTEMA DE NAVEGAÇÃO SUPERIOR (DASHBOARD FLOW) ---
st.markdown('<div style="text-align: center; font-weight: bold; color: #3b82f6; margin-top: 15px; font-size: 14px; letter-spacing: 2px;">TECHNOBOLT AI COMMAND CENTER</div>', unsafe_allow_html=True)

menu_opcoes = [
    "🏠 Dashboard Inicial", 
    "📁 Analisador de Documentos & Contratos",
    "✉️ Gerador de Email Inteligente", 
    "🧠 Briefing Negocial Estratégico", 
    "📝 Analista de Atas de Governança",
    "📈 Inteligência Competitiva & Churn"
]
menu_selecionado = st.selectbox("Selecione o Módulo Ativo", menu_opcoes, label_visibility="collapsed")
st.markdown("<hr>", unsafe_allow_html=True)

# --- 5. GESTÃO DE ESTADO (MEMÓRIA DO APP) ---
if 'tags' not in st.session_state:
    st.session_state.tags = ["Novas Leis", "Concorrência", "Inovação Tech", "Cenário Macro", "ESG"]

# --- 6. TELAS DETALHADAS ---

# --- TELA: DASHBOARD ---
if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #9ca3af !important; font-size: 18px;'>Plataforma Unificada de Inteligência Corporativa Sênior.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📄 Documentos\nAnálise técnica traduzida para visão de gestão e riscos.")
    with col2:
        st.markdown("### ✉️ Comunicação\nRedação de e-mails executivos com precisão tonal.")
    with col3:
        st.markdown("### 📊 Inteligência\nMonitoramento de mercado e prevenção de perda de clientes.")
    
    st.markdown("---")
    st.markdown("""
    **Como utilizar este Hub:**
    1. Utilize o menu superior para alternar entre as ferramentas.
    2. No **Analisador**, faça upload de arquivos para obter relatórios "McKinsey Style".
    3. Na **Inteligência**, insira nomes de rivais para encontrar brechas comerciais.
    """)

# --- TELA: ANALISADOR DE DOCUMENTOS ---
elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos & Tradutor de Gestão</h1><p>Suporte para PDF, DOCX e TXT</p></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Suba um relatório técnico, contrato ou proposta comercial:", type=["pdf", "docx", "txt"])
    
    if arquivo:
        if st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
            with st.spinner("Gemini 3 Flash analisando complexidade técnica..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    if arquivo.type == "application/pdf":
                        conteudo_ia = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        texto = extrair_texto_docx(arquivo)
                        conteudo_ia = [f"Analise este conteúdo de um arquivo Word:\n\n{texto}"]
                    else:
                        conteudo_ia = [arquivo.read().decode("utf-8")]

                    prompt = """
                    Você é um Consultor Estratégico Sênior. Analise o documento e gere um relatório executivo:
                    - **RESUMO EXECUTIVO:** O que é o documento em 3 parágrafos.
                    - **ANÁLISE DE IMPACTO:** Traduza para Riscos, Custos Estimados e Oportunidades.
                    - **PONTOS CRÍTICOS:** O que o CEO/Diretor não pode ignorar.
                    - **PLANO DE AÇÃO:** 3 passos imediatos baseados em boas práticas de mercado.
                    - **RESPOSTA SUGERIDA:** Um rascunho de e-mail formal de feedback.
                    """
                    response = model.generate_content([prompt] + conteudo_ia)
                    st.markdown("---")
                    st.markdown(response.text)
                    st.download_button("📥 Exportar Relatório (.md)", response.text, file_name="relatorio_technobolt.md")
                except Exception as e: st.error(f"Erro no processamento: {e}")

# --- TELA: EMAIL ---
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1><p>Redação executiva de alto impacto</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: cargo = st.text_input("Cargo da IA:", placeholder="Ex: Diretor Financeiro (CFO)")
    with c2: dest = st.text_input("Para quem:", placeholder="Ex: Conselho Consultivo")
    obj = st.text_area("Objetivo Central:", placeholder="Ex: Justificar a necessidade de aporte no projeto de expansão...")
    formalidade = st.select_slider("Grau de Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    
    if st.button("🚀 GERAR COMUNICAÇÃO"):
        with st.spinner("IA redigindo conteúdo profissional..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_e = f"Como {cargo}, escreva para {dest} sobre {obj}. Use tom {formalidade}. Seja conciso e direto."
                res = model.generate_content(prompt_e)
                st.text_area("Cópia disponível:", res.text, height=400)
            except Exception as e: st.error(f"Erro: {e}")

# --- TELA: BRIEFING ---
elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Negocial Estratégico</h1><p>Radar de mercado em tempo real</p></div>', unsafe_allow_html=True)
    emp = st.text_input("Empresa Alvo:")
    set = st.text_input("Setor de Atuação:")
    tags_s = st.multiselect("Filtros de Inteligência:", options=st.session_state.tags, default=["Novas Leis"])
    nova = st.text_input("➕ Adicionar Novo Filtro:")
    if nova and nova not in st.session_state.tags:
        st.session_state.tags.append(nova)
        st.rerun()
    
    if st.button("⚡ ESCANEAR MERCADO"):
        with st.spinner("Analisando tendências e notícias..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_b = f"Gere um briefing executivo para {emp} no setor {set} focando em {tags_s}."
                res = model.generate_content(prompt_b)
                st.markdown(res.text)
            except Exception as e: st.error(e)

# --- TELA: ATAS ---
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas de Governança</h1><p>Formalização ágil de deliberações</p></div>', unsafe_allow_html=True)
    txt_ata = st.text_area("Notas brutas da reunião (quem participou, o que foi decidido):", height=300)
    if st.button("📝 FORMALIZAR DOCUMENTO"):
        with st.spinner("Estruturando ata formal..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                res = model.generate_content(f"Transforme estas notas em uma ata formal de diretoria estruturada: {txt_ata}")
                st.markdown(res.text)
            except Exception as e: st.error(e)

# --- TELA: INTELIGÊNCIA COMPETITIVA ---
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência Competitiva & Churn</h1><p>Proteção de base e análise de rivais</p></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Radar de Rivais", "⚠️ Previsão de Perda (Churn)"])
    
    with t1:
        rival_n = st.text_input("Nome do Concorrente:")
        if st.button("📡 ANALISAR MOVIMENTAÇÕES"):
            with st.spinner("Cruzando dados de mercado..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    res = model.generate_content(f"Analise a estratégia atual da {rival_n} e aponte brechas comerciais.")
                    st.markdown(res.text)
                except Exception as e: st.error(e)
                
    with t2:
        feed = st.text_area("Feedback ou histórico de reclamação do cliente:")
        if st.button("🧠 AVALIAR RISCO"):
            with st.spinner("Analisando sentimento..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    res = model.generate_content(f"Analise o risco de perda (0-100%) baseado neste feedback: {feed}")
                    st.markdown(res.text)
                except Exception as e: st.error(e)

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Enterprise Edition v3.4 (Strategic Dark)")