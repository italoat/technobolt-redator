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

# --- 2. CSS ULTRA-BLINDADO (CORREÇÃO DE FUNDOS E TEXTOS ESCUROS) ---
st.markdown("""
<style>
    /* 1. FUNDO ESCURO GLOBAL ABSOLUTO EM TODOS OS NÍVEIS */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
    .stApp, [data-testid="stMain"], [data-testid="stVerticalBlock"],
    [data-testid="stMarkdownContainer"], .main, [data-testid="stBlock"],
    div[role="dialog"], div[data-baseweb="popover"], [data-testid="stExpander"] {
        background-color: #0d1117 !important;
        color: #ffffff !important;
    }

    /* 2. REMOÇÃO DE ELEMENTOS NATIVOS E CABEÇALHOS DO STREAMLIT */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* 3. FORÇA TODAS AS FONTES PARA BRANCO (ESTADO ATIVO E INATIVO) */
    h1, h2, h3, h4, h5, h6, p, label, span, div, .stMarkdown, 
    [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p,
    [data-testid="stHeader"], .stSelectbox label, .stTextInput label,
    .stTextArea label, [data-testid="stMetricValue"], 
    input, textarea, [data-baseweb="select"] * { 
        color: #ffffff !important; 
        -webkit-text-fill-color: #ffffff !important;
    }

    /* 4. TÍTULO E CABEÇALHOS CORPORATIVOS CUSTOMIZADOS */
    .main-title { 
        font-size: 38px; font-weight: 900; text-align: center; 
        margin-top: 10px; margin-bottom: 5px; color: #ffffff !important;
        letter-spacing: -1.5px;
    }
    .product-header { 
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%); 
        padding: 30px; border-radius: 18px; margin-bottom: 30px; 
        text-align: center; border: 1px solid #374151;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }

    /* 5. CORREÇÃO DA BARRA DE SERVIÇOS (SELECTBOX) E MENU SUSPENSO */
    div[data-baseweb="select"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
    }
    
    /* Fundo da lista aberta e itens (evita o branco) */
    div[data-baseweb="popover"] > div, ul[role="listbox"], [data-baseweb="listbox"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
    }
    
    li[role="option"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
    }
    
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }

    /* 6. INPUTS E TEXTAREAS (GARANTE QUE O TEXTO DIGITADO SEJA BRANCO) */
    .stTextInput input, .stTextArea textarea {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* 7. BOTÕES EXECUTIVOS PREMIUM (REMOÇÃO DE FAIXAS E BORDAS PRETAS) */
    .stButton > button { 
        width: 100%; border-radius: 12px; height: 4.2em; font-weight: bold; 
        background-color: #238636 !important; /* Cor Verde Sólida */
        color: #ffffff !important; 
        border: none !important;
        outline: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #2ea043 !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(35, 134, 54, 0.4) !important;
        border: none !important;
    }
    
    .stButton > button:focus, .stButton > button:active {
        background-color: #238636 !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /* 8. ÁREA DE UPLOAD E ABAS (TABS) */
    [data-testid="stFileUploader"] section {
        background-color: #161b22 !important;
        border: 2px dashed #30363d !important;
        border-radius: 15px;
        padding: 20px;
        color: #ffffff !important;
    }
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: 700; }
    
    /* 9. SLIDERS E TAGS */
    .stSlider label, .stSlider span { color: #ffffff !important; }
    span[data-baseweb="tag"] { background-color: #1d4ed8 !important; color: #ffffff !important; border-radius: 5px; }

    hr { border: 0.5px solid #30363d !important; margin: 30px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE: CONFIGURAÇÃO DA API E MODELO ---
api_key = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "models/gemini-3-flash-preview"

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Configuração Pendente: GEMINI_API_KEY não encontrada nas variáveis de ambiente.")

def extrair_texto_docx(arquivo_docx):
    """Extração de texto para suporte total a documentos Microsoft Word (.docx)."""
    doc = docx.Document(arquivo_docx)
    return "\n".join([para.text for para in doc.paragraphs])

# --- 4. SISTEMA DE NAVEGAÇÃO SUPERIOR (COMMAND CENTER) ---
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

# --- 5. GESTÃO DE ESTADO (MEMÓRIA DE TAGS E SESSÃO) ---
if 'tags' not in st.session_state:
    st.session_state.tags = ["Novas Leis", "Concorrência", "Inovação Tech", "Cenário Macro", "ESG"]

# --- 6. TELAS DO HUB ---

# --- TELA: DASHBOARD INICIAL ---
if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #9ca3af !important; font-size: 18px;'>Plataforma Unificada de Inteligência Corporativa Sênior.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📄 Documentos\nResumos executivos focados em traduzir complexidade técnica para Riscos, Custos e Ações estratégicas.")
    with col2:
        st.markdown("### ✉️ Comunicação\nRedação de e-mails executivos de alto impacto com ajuste fino de cargo, destinatário e tom profissional.")
    with col3:
        st.markdown("### 📊 Inteligência\nMonitoramento competitivo de rivais e análise de sentimento para prevenção ativa de perda de clientes (Churn).")
    
    st.markdown("---")
    st.markdown("""
    ### 🛠️ Guia de Operação Corporativa:
    1. **Navegação Inteligente:** Utilize o menu suspenso central no topo para alternar entre as ferramentas.
    2. **Analisador:** Faça upload de arquivos **PDF, DOCX ou TXT**. O sistema processa o conteúdo sob a ótica de um Consultor Sênior.
    3. **Briefing Negocial:** Ideal para panoramas rápidos. Informe empresa e setor para receber um radar de mercado 2025.
    4. **Governança:** Utilize o Analista de Atas para formalizar reuniões complexas a partir de anotações brutas de diretoria.
    5. **Prevenção:** Use a aba de Churn para colar e-mails críticos de clientes e receber estratégias imediatas de retenção.
    """)

# --- TELA: ANALISADOR DE DOCUMENTOS ---
elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos & Tradutor de Gestão</h1><p>Processamento inteligente para PDF, DOCX (Word) e TXT</p></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Suba o relatório técnico, contrato ou proposta comercial:", type=["pdf", "docx", "txt"])
    
    if arquivo:
        if st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
            with st.spinner("IA processando inteligência técnica e traduzindo para visão executiva..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    
                    if arquivo.type == "application/pdf":
                        conteudo_ia = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        texto_w = extrair_texto_docx(arquivo)
                        conteudo_ia = [f"Analise estrategicamente este conteúdo extraído de um documento Word:\n\n{texto_w}"]
                    else:
                        conteudo_ia = [arquivo.read().decode("utf-8")]

                    prompt_doc = """
                    Você é um Consultor de Estratégia Sênior (ex-McKinsey). Analise o documento em anexo e produza um relatório executivo estruturado:
                    - **RESUMO EXECUTIVO:** Do que se trata o documento em linguagem simples e executiva.
                    - **ANÁLISE DE IMPACTO:** Traduza termos técnicos para RISCO, CUSTO ESTIMADO e OPORTUNIDADES.
                    - **PONTOS CRÍTICOS:** O que o gestor NÃO pode ignorar sob nenhuma hipótese.
                    - **PLANO DE AÇÃO:** 3 passos imediatos sugeridos baseados em boas práticas de mercado.
                    - **SUGESTÃO DE RESPOSTA:** Um rascunho de e-mail ou feedback formal para o autor do documento.
                    """
                    response = model.generate_content([prompt_doc] + conteudo_ia)
                    st.markdown("---")
                    st.markdown("### 📊 Resultado da Análise Gerencial")
                    st.markdown(response.text)
                    st.download_button("📥 Baixar Relatório (.md)", response.text, file_name="analise_technobolt.md")
                except Exception as e: st.error(f"Erro no processamento do arquivo: {e}")

# --- TELA: GERADOR DE EMAIL ---
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1><p>Redação executiva de alto impacto e tom ajustável</p></div>', unsafe_allow_html=True)
    col_em1, col_em2 = st.columns(2)
    with col_em1: cargo = st.text_input("Seu Cargo:", placeholder="Ex: Diretor de Operações")
    with col_em2: dest = st.text_input("Destinatário:", placeholder="Ex: CEO da Holding")
    obj = st.text_area("Objetivo Central da Mensagem:", placeholder="Ex: Justificar a necessidade de aporte no projeto de expansão...")
    formalidade = st.select_slider("Grau de Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    
    if st.button("🚀 GERAR COMUNICAÇÃO PROFISSIONAL"):
        with st.spinner("IA redigindo conteúdo profissional estratégico..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_email = f"Como {cargo}, escreva um e-mail para {dest} focado em {obj}. Utilize um tom {formalidade}. Seja conciso e persuasivo."
                res = model.generate_content(prompt_email)
                st.text_area("Rascunho disponível para uso:", res.text, height=450)
            except Exception as e: st.error(f"Erro na geração do e-mail: {e}")

# --- TELA: BRIEFING NEGOCIAL ---
elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Negocial Estratégico</h1><p>Radar de mercado em tempo real e monitoramento de tendências</p></div>', unsafe_allow_html=True)
    c_b1, c_b2 = st.columns(2)
    with c_b1: empresa_alvo = st.text_input("Nome da Empresa Alvo:")
    with c_b2: setor_atuacao = st.text_input("Setor de Atuação:")
    
    tags_s = st.multiselect("Pilares do Radar de Inteligência:", options=st.session_state.tags, default=["Novas Leis", "Concorrência"])
    
    nova_tag = st.text_input("➕ Adicionar Novo Filtro ao seu Radar Personalizado:")
    if nova_tag and nova_tag not in st.session_state.tags:
        st.session_state.tags.append(nova_tag)
        st.rerun()
    
    if st.button("⚡ ESCANEAR MERCADO E TENDÊNCIAS"):
        with st.spinner("Cruzando notícias e dados estratégicos de 2025..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_briefing = f"Gere um briefing executivo para a empresa {empresa_alvo} no setor {setor_atuacao} focando nos seguintes pilares estratégicos: {tags_s}."
                res = model.generate_content(prompt_briefing)
                st.markdown(res.text)
            except Exception as e: st.error(f"Erro no briefing: {e}")

# --- TELA: ANALISTA DE ATAS ---
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas de Governança</h1><p>Formalização ágil de deliberações a partir de notas brutas</p></div>', unsafe_allow_html=True)
    notas_brutas = st.text_area("Insira as notas brutas da reunião (Participantes, tópicos, deliberações):", height=300)
    if st.button("📝 FORMALIZAR DOCUMENTO"):
        with st.spinner("IA estruturando ata de diretoria em formato oficial..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                res_ata = model.generate_content(f"Transforme estas notas em uma ata formal de diretoria estruturada: {notas_brutas}")
                st.markdown(res_ata.text)
            except Exception as e: st.error(f"Erro na ata: {e}")

# --- TELA: INTELIGÊNCIA COMPETITIVA ---
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência Competitiva & Churn</h1><p>Análise estratégica de rivais e proteção de base de clientes</p></div>', unsafe_allow_html=True)
    t_rival, t_churn = st.tabs(["🔍 Radar de Rivais", "⚠️ Previsão de Perda (Churn)"])
    
    with t_rival:
        nome_rival = st.text_input("Nome da Empresa Concorrente:")
        if st.button("📡 ANALISAR MOVIMENTAÇÕES DO RIVAL"):
            with st.spinner("Analisando brechas comerciais e movimentos do mercado..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    res_riv = model.generate_content(f"Analise a estratégia recente da empresa {nome_rival} e identifique vulnerabilidades.")
                    st.markdown(res_riv.text)
                except Exception as e: st.error(e)
                
    with t_churn:
        feedback_cli = st.text_area("Insira o feedback crítico do cliente ou reclamação:")
        if st.button("🧠 AVALIAR RISCO DE SAÍDA"):
            with st.spinner("Analisando sentimento e probabilidade de perda..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    res_ch = model.generate_content(f"Com base neste feedback, avalie o risco de churn (0 a 100%) e sugira uma ação de retenção: {feedback_cli}")
                    st.markdown(res_ch.text)
                except Exception as e: st.error(e)

# --- RODAPÉ CORPORATIVO ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Enterprise Strategic Edition v4.8 (Full Unabridged Code)")