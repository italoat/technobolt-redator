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

# --- 2. CSS ULTRA-PREMIUM (BLINDAGEM CONTRA FUNDO BRANCO E FAIXAS) ---
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

    /* 3. FORÇA FONTES BRANCAS EM TUDO (MESMO DENTRO DE COMPONENTES) */
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

    /* 6. INPUTS E TEXTAREAS (CINZA ESCURO #161b22) */
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
        padding: 10px 25px !important;
        font-weight: 700 !important;
    }

    /* 8. BOTÕES EXECUTIVOS (VERDE VIBRANTE SEM FAIXA PRETA) */
    .stButton > button { 
        width: 100%; border-radius: 14px; height: 4.5em; font-weight: 700; 
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: none !important;
        outline: none !important;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.2) !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .stButton > button:hover, .stButton > button:focus, .stButton > button:active {
        background-color: #2ea043 !important;
        color: #ffffff !important;
        border: none !important;
        outline: none !important;
        box-shadow: 0 20px 25px -5px rgba(16, 185, 129, 0.4) !important;
        transform: translateY(-2px);
    }

    /* 9. SLIDER DE FORMALIDADE E TABS */
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
    """Lê arquivos Word (.docx) e extrai o texto de forma estruturada."""
    doc = docx.Document(arquivo_docx)
    return "\n".join([para.text for para in doc.paragraphs])

# --- 4. SISTEMA DE NAVEGAÇÃO SUPERIOR (COMMAND CENTER) ---
st.markdown('<div style="text-align: center; font-weight: 700; color: #94a3b8; margin-top: 20px; font-size: 12px; letter-spacing: 4px; text-transform: uppercase;">Command Center v7.4</div>', unsafe_allow_html=True)

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

# --- 5. GESTÃO DE ESTADO (MEMÓRIA DE TAGS) ---
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
        st.markdown("### ✉️ Comunicação\nRedação de e-mails executivos de alto impacto com ajuste fino de tom estratégico.")
    with col3:
        st.markdown("### 📊 Inteligência\nMonitoramento competitivo de rivais e análise de sentimento para prevenção de Churn.")
    
    st.markdown("---")
    st.markdown("""
    ### 🛠️ Guia de Operação Corporativa:
    1. **Navegação:** Utilize o menu no topo para alternar entre os 6 módulos integrados.
    2. **Analisador:** Faça upload de arquivos **PDF, DOCX ou TXT**. Processamento McKinsey-style.
    3. **Briefing:** Informe empresa e setor para receber um radar de mercado 2025 completo.
    4. **Atas:** Formalize reuniões complexas a partir de anotações brutas de diretoria.
    5. **Prevenção:** Cole feedbacks críticos para receber estratégias imediatas de retenção de clientes.
    """)

elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos & Tradutor de Gestão</h1><p>Processamento inteligente para PDF, DOCX (Word) e TXT</p></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Suba o relatório técnico ou contrato comercial:", type=["pdf", "docx", "txt"])
    
    if arquivo:
        if st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
            with st.spinner("IA processando inteligência técnica e traduzindo para gestão..."):
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
                    Você é um Consultor de Estratégia Sênior (ex-McKinsey). Analise o documento em anexo e produza um relatório executivo:
                    - **RESUMO EXECUTIVO:** Do que se trata o documento de forma simples e executiva.
                    - **ANÁLISE DE IMPACTO:** Traduza termos técnicos para RISCO, CUSTO ESTIMADO e OPORTUNIDADES.
                    - **PONTOS CRÍTICOS:** O que o gestor NÃO pode ignorar sob nenhuma hipótese.
                    - **PLANO DE AÇÃO:** 3 passos imediatos sugeridos baseados em boas práticas de mercado.
                    - **SUGESTÃO DE RESPOSTA:** Um rascunho de e-mail ou feedback formal para o autor do documento.
                    """
                    response = model.generate_content([prompt_doc] + c_ia)
                    st.markdown("---")
                    st.markdown("### 📊 Resultado da Análise Gerencial")
                    st.markdown(response.text)
                except Exception as e: st.error(f"Erro no processamento: {e}")

elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1><p>Redação executiva estratégica</p></div>', unsafe_allow_html=True)
    c_e1, c_e2 = st.columns(2)
    with c_e1: cargo = st.text_input("Seu Cargo:", placeholder="Ex: Diretor de Operações")
    with c_e2: dest = st.text_input("Destinatário:", placeholder="Ex: CEO da Holding")
    obj = st.text_area("Objetivo da Mensagem:", placeholder="Ex: Justificar aumento de orçamento para o projeto X...")
    formalidade = st.select_slider("Grau de Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    
    if st.button("🚀 GERAR COMUNICAÇÃO PROFISSIONAL"):
        with st.spinner("IA redigindo conteúdo profissional estratégico..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_email = f"Como {cargo}, escreva um e-mail para {dest} focado em {obj}. Tom {formalidade}. Seja persuasivo e conciso."
                res = model.generate_content(prompt_email)
                st.text_area("Rascunho disponível para uso imediato:", res.text, height=450)
            except Exception as e: st.error(f"Erro: {e}")

elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Negocial Estratégico</h1><p>Radar de mercado e monitoramento de tendências</p></div>', unsafe_allow_html=True)
    c_b1, c_b2 = st.columns(2)
    with c_b1: empresa = st.text_input("Empresa Alvo:")
    with c_b2: setor = st.text_input("Setor de Atuação:")
    tags_s = st.multiselect("Radar de Inteligência:", options=st.session_state.tags, default=["Novas Leis", "Concorrência"])
    
    if st.button("⚡ ESCANEAR MERCADO E TENDÊNCIAS"):
        with st.spinner("Analisando notícias globais..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_b = f"Gere um briefing executivo para a empresa {empresa} no setor {setor} focado em {tags_s}."
                res = model.generate_content(prompt_b)
                st.markdown(res.text)
            except Exception as e: st.error(e)

elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência Competitiva & Churn</h1><p>Análise estratégica de rivais e proteção de base</p></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Radar Rival", "⚠️ Previsão de Churn"])
    with t1:
        rival = st.text_input("Nome do Rival:")
        if st.button("📡 ANALISAR MOVIMENTAÇÕES"):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Analise a estratégia recente da empresa {rival} e identifique brechas.")
            st.markdown(res.text)
    with t2:
        feed = st.text_area("Feedback crítico do cliente:")
        if st.button("🧠 AVALIAR RISCO"):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Avalie o risco de churn (0 a 100%) baseado neste feedback: {feed}")
            st.markdown(res.text)

# --- RODAPÉ CORPORATIVO ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | obsidian Interface v7.4")