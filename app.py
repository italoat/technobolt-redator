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

# --- 2. CSS ULTRA-PREMIUM (CORREÇÕES VISUAIS E BLINDAGEM DARK) ---
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

    /* 2. REMOÇÃO DE ELEMENTOS NATIVOS E CABEÇALHOS */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* 3. FORÇA TODAS AS FONTES E LABELS PARA BRANCO */
    * { 
        color: #ffffff !important; 
        -webkit-text-fill-color: #ffffff !important;
    }

    /* 4. TÍTULO E CABEÇALHOS CORPORATIVOS */
    .main-title { 
        font-size: 42px; font-weight: 900; text-align: center; 
        margin-top: 10px; margin-bottom: 5px; color: #ffffff !important;
        letter-spacing: -1.5px;
    }
    .product-header { 
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); 
        padding: 35px; border-radius: 20px; margin-bottom: 35px; 
        text-align: center; border: 1px solid #334155;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }

    /* 5. ESTILIZAÇÃO DA LISTA SUSPENSA (MENU) - VISUAL ATRATIVO */
    div[data-baseweb="select"] {
        background-color: #161b22 !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 12px !important;
        padding: 5px !important;
    }
    
    /* Fundo da lista aberta (popover) */
    div[data-baseweb="popover"] > div, ul[role="listbox"], [data-baseweb="listbox"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
    }
    
    /* Itens da lista com hover animado */
    li[role="option"] {
        background-color: transparent !important;
        color: #ffffff !important;
        padding: 12px !important;
        margin: 4px !important;
        border-radius: 8px !important;
        transition: 0.3s all ease;
    }
    
    li[role="option"]:hover {
        background-color: #1d4ed8 !important; /* Azul Destaque */
        transform: translateX(8px);
    }

    /* 6. CORREÇÃO DO BOTÃO "BROWSE FILES" (UPLOADER) */
    [data-testid="stFileUploader"] button {
        background-color: #3b82f6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        font-weight: bold !important;
    }
    
    [data-testid="stFileUploader"] section {
        background-color: #161b22 !important;
        border: 2px dashed #3b82f6 !important;
        border-radius: 15px !important;
        padding: 25px !important;
    }

    /* 7. CORREÇÃO DOS BOTÕES (VERDE SEM FAIXAS OU FUNDO PRETO) */
    .stButton > button { 
        width: 100%; border-radius: 15px; height: 4.5em; font-weight: bold; 
        background-color: #238636 !important; /* Verde Vibrante */
        color: #ffffff !important; 
        border: none !important;
        outline: none !important;
        box-shadow: 0 4px 15px rgba(35, 134, 54, 0.3) !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        transition: all 0.3s ease-in-out;
    }
    
    .stButton > button:hover, .stButton > button:focus, .stButton > button:active {
        background-color: #2ea043 !important;
        color: #ffffff !important;
        border: none !important;
        outline: none !important;
        box-shadow: 0 8px 20px rgba(35, 134, 54, 0.5) !important;
        transform: translateY(-2px);
    }

    /* 8. INPUTS E TEXTAREAS (TEXTO SEMPRE BRANCO) */
    .stTextInput input, .stTextArea textarea {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* 9. TABS E SLIDERS */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: 700; font-size: 16px; }
    .stSlider label, .stSlider span { color: #ffffff !important; }
    span[data-baseweb="tag"] { background-color: #1d4ed8 !important; color: #ffffff !important; border-radius: 5px; }

    hr { border: 0.5px solid #334155 !important; margin: 30px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE: CONFIGURAÇÃO DA API E MODELO ---
api_key = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "models/gemini-3-flash-preview"

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Configuração Necessária: GEMINI_API_KEY não encontrada.")

def extrair_texto_docx(arquivo_docx):
    """Lê arquivos Word (.docx) e extrai o texto de forma estruturada."""
    doc = docx.Document(arquivo_docx)
    return "\n".join([para.text for para in doc.paragraphs])

# --- 4. SISTEMA DE NAVEGAÇÃO SUPERIOR (COMMAND CENTER) ---
st.markdown('<div style="text-align: center; font-weight: bold; color: #60a5fa; margin-top: 15px; font-size: 14px; letter-spacing: 3px; text-transform: uppercase;">TechnoBolt AI Command Center</div>', unsafe_allow_html=True)

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

# --- 5. GESTÃO DE ESTADO (PERSISTÊNCIA DE SESSÃO) ---
if 'tags' not in st.session_state:
    st.session_state.tags = ["Novas Leis", "Concorrência", "Inovação Tech", "Cenário Macro", "ESG", "M&A"]

# --- 6. TELAS DO HUB ---

# --- TELA: DASHBOARD INICIAL ---
if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #9ca3af !important; font-size: 18px;'>Plataforma Unificada de Inteligência Corporativa para Alta Gestão.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📄 Documentos\nAnalise contratos e relatórios complexos traduzindo termos técnicos para uma visão de Riscos, Custos e Ações estratégicas.")
    with col2:
        st.markdown("### ✉️ Comunicação\nCrie e-mails executivos de alto nível em segundos, ajustando cargo e tom para garantir a melhor percepção.")
    with col3:
        st.markdown("### 📊 Inteligência\nMonitore movimentos da concorrência e utilize IA para prever riscos de cancelamento através do sentimento do cliente.")
    
    st.markdown("---")
    st.markdown("""
    ### 🛠️ Guia de Operação:
    1. **Navegação:** Utilize o menu suspenso centralizado no topo para alternar entre os 6 módulos.
    2. **Analisador:** Faça upload de arquivos **PDF, DOCX ou TXT**. O sistema processa o conteúdo sob a ótica de um Consultor Sênior.
    3. **Briefing Negocial:** Ideal para reuniões. Informe a empresa e o setor para receber um panorama de mercado atualizado.
    4. **Governança:** Utilize o Analista de Atas para formalizar reuniões complexas a partir de anotações brutas.
    5. **Prevenção:** Use a aba de Churn para colar e-mails críticos e receber estratégias imediatas de retenção.
    """)

# --- TELA: ANALISADOR DE DOCUMENTOS ---
elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos & Tradutor de Gestão</h1><p>Suporte Universal para PDF, DOCX (Word) e TXT</p></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Suba o documento técnico, contrato ou proposta estratégica:", type=["pdf", "docx", "txt"])
    
    if arquivo:
        if st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
            with st.spinner("Gemini 3 Flash analisando dados e gerando inteligência..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    if arquivo.type == "application/pdf":
                        conteudo_ia = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        texto_w = extrair_texto_docx(arquivo)
                        conteudo_ia = [f"Analise estrategicamente este conteúdo extraído de um Word:\n\n{texto_word}"]
                    else:
                        conteudo_ia = [arquivo.read().decode("utf-8")]

                    prompt_doc = """
                    Atue como um Consultor Estratégico Sênior. Analise o documento e gere um relatório executivo:
                    - **RESUMO EXECUTIVO:** Do que se trata o documento de forma direta.
                    - **ANÁLISE DE IMPACTO:** Traduza para RISCO, CUSTO ESTIMADO e OPORTUNIDADES.
                    - **PONTOS CRÍTICOS:** O que o gestor NÃO pode ignorar.
                    - **PLANO DE AÇÃO:** 3 passos imediatos sugeridos.
                    - **SUGESTÃO DE RESPOSTA:** Um rascunho de e-mail formal de feedback.
                    """
                    response = model.generate_content([prompt_doc] + conteudo_ia)
                    st.markdown("---")
                    st.markdown("### 📊 Relatório de Inteligência Gerado")
                    st.markdown(response.text)
                    st.download_button("📥 Exportar Relatório para MD", response.text, file_name="analise_technobolt.md")
                except Exception as e: st.error(f"Erro no processamento: {e}")

# --- TELA: GERADOR DE EMAIL ---
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1><p>Comunicação executiva precisa e estratégica</p></div>', unsafe_allow_html=True)
    col_em1, col_em2 = st.columns(2)
    with col_em1: cargo_user = st.text_input("Seu Cargo:", placeholder="Ex: Diretor Financeiro")
    with col_em2: dest_user = st.text_input("Destinatário:", placeholder="Ex: Investidores")
    objetivo_msg = st.text_area("Objetivo Central da Mensagem:", placeholder="Ex: Solicitar aprovação de orçamento...")
    formalidade = st.select_slider("Grau de Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    
    if st.button("🚀 GERAR COMUNICAÇÃO PROFISSIONAL"):
        with st.spinner("IA redigindo conteúdo profissional..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_email = f"Como {cargo_user}, escreva um e-mail para {dest_user} sobre {objetivo_msg}. Tom {formalidade}."
                res = model.generate_content(prompt_email)
                st.text_area("Cópia disponível para uso:", res.text, height=450)
            except Exception as e: st.error(f"Erro na geração: {e}")

# --- TELA: BRIEFING NEGOCIAL ---
elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Negocial Estratégico</h1><p>Radar de mercado e tendências</p></div>', unsafe_allow_html=True)
    c_b1, c_b2 = st.columns(2)
    with c_b1: empresa_nome = st.text_input("Empresa Alvo:")
    with c_b2: setor_nome = st.text_input("Setor de Atuação:")
    
    tags_ativas = st.multiselect("Filtros do Radar:", options=st.session_state.tags, default=["Novas Leis", "Concorrência"])
    
    nova_tag_req = st.text_input("➕ Adicionar Novo Filtro ao Radar:")
    if nova_tag_req and nova_tag_req not in st.session_state.tags:
        st.session_state.tags.append(nova_tag_req)
        st.rerun()
    
    if st.button("⚡ ESCANEAR MERCADO E TENDÊNCIAS"):
        with st.spinner("Analisando notícias 2025..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_brief = f"Briefing executivo para {empresa_nome} em {setor_nome} focado em {tags_ativas}."
                res_brief = model.generate_content(prompt_brief)
                st.markdown(res_brief.text)
            except Exception as e: st.error(e)

# --- TELA: ANALISTA DE ATAS ---
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas de Governança</h1><p>Formalização de reuniões</p></div>', unsafe_allow_html=True)
    notas_reuniao = st.text_area("Insira as notas brutas da reunião:", height=300)
    if st.button("📝 GERAR ATA OFICIAL"):
        with st.spinner("IA estruturando documento..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                res_ata = model.generate_content(f"Transforme em ata formal: {notas_reuniao}")
                st.markdown(res_ata.text)
            except Exception as e: st.error(e)

# --- TELA: INTELIGÊNCIA COMPETITIVA ---
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência Competitiva & Churn</h1><p>Análise de rivais e proteção de base</p></div>', unsafe_allow_html=True)
    tab_rival, tab_churn = st.tabs(["🔍 Radar de Concorrência", "⚠️ Previsão de Churn"])
    
    with tab_rival:
        nome_concorrente = st.text_input("Nome do Rival:")
        if st.button("📡 ANALISAR ESTRATÉGIA"):
            model = genai.GenerativeModel(MODEL_NAME)
            res_riv = model.generate_content(f"Analise a estratégia da {nome_concorrente}.")
            st.markdown(res_riv.text)
                
    with tab_churn:
        texto_feedback = st.text_area("Feedback do cliente:")
        if st.button("🧠 AVALIAR RISCO"):
            model = genai.GenerativeModel(MODEL_NAME)
            res_ch = model.generate_content(f"Avalie risco de churn para: {texto_feedback}")
            st.markdown(res_ch.text)

# --- RODAPÉ CORPORATIVO ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Enterprise Strategic Edition v5.2 (Full & Unabridged)")