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

# --- 2. CSS ULTRA-BLINDADO (DARK MODE TOTAL & CORREÇÃO DE COMPONENTES) ---
st.markdown("""
<style>
    /* 1. FUNDO ESCURO GLOBAL ABSOLUTO (PINTA TODAS AS CAMADAS DO STREAMLIT) */
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

    /* 3. FORÇA TODAS AS FONTES E LABELS PARA BRANCO (SEM EXCEÇÃO) */
    h1, h2, h3, h4, h5, h6, p, label, span, div, .stMarkdown, 
    [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p,
    [data-testid="stHeader"], .stSelectbox label, .stTextInput label,
    .stTextArea label, [data-testid="stMetricValue"], [data-baseweb="select"],
    [data-testid="stFileUploadDropzone"] div { 
        color: #ffffff !important; 
    }

    /* 4. TÍTULO E CABEÇALHOS CORPORATIVOS CUSTOMIZADOS */
    .main-title { 
        font-size: 42px; font-weight: 900; text-align: center; 
        margin-top: 10px; margin-bottom: 5px; color: #ffffff !important;
        letter-spacing: -1.5px;
    }
    .product-header { 
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%); 
        padding: 35px; border-radius: 18px; margin-bottom: 35px; 
        text-align: center; border: 1px solid #374151;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }

    /* 5. CORREÇÃO DA BARRA DE SERVIÇOS (SELECTBOX) E MENU SUSPENSO */
    /* Fundo do campo selectbox fechado */
    div[data-baseweb="select"] > div {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
    }
    
    /* Fundo da lista suspensa (aberta) - Ataca a camada flutuante */
    div[data-baseweb="popover"] > div, ul[role="listbox"], [data-baseweb="listbox"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
    }
    
    /* Itens individuais da lista suspensa */
    li[role="option"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        transition: background 0.2s;
    }
    
    /* Hover e Seleção na lista */
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }

    /* 6. CORREÇÃO DOS BOTÕES (VERDE COLORIDO E SEM FAIXA PRETA) */
    .stButton > button { 
        width: 100%; border-radius: 15px; height: 4.2em; font-weight: bold; 
        background-color: #238636 !important; /* Cor Verde Base */
        color: #ffffff !important; 
        border: none !important;
        outline: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        transition: all 0.3s ease-in-out;
    }
    
    /* Hover e Focus: Mantém a cor colorida e remove fundos pretos residuais */
    .stButton > button:hover {
        background-color: #2ea043 !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(35, 134, 54, 0.4) !important;
    }
    
    .stButton > button:focus, .stButton > button:active {
        background-color: #238636 !important;
        color: #ffffff !important;
        border: none !important;
        outline: none !important;
    }

    /* 7. CUSTOMIZAÇÃO DE INPUTS E TEXTAREAS */
    .stTextInput input, .stTextArea textarea {
        background-color: #0d1117 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* 8. TABS, SLIDERS E UPLOAD */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: 700; font-size: 16px; }
    
    [data-testid="stFileUploader"] section {
        background-color: #161b22 !important;
        border: 2px dashed #30363d !important;
        border-radius: 15px;
        color: #ffffff !important;
    }
    
    .stSlider label, .stSlider span { color: #ffffff !important; }
    
    hr { border: 0.5px solid #30363d !important; margin: 30px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE: CONFIGURAÇÃO DA API E MODELO ---
api_key = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "models/gemini-3-flash-preview"

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Configuração Necessária: Defina a variável GEMINI_API_KEY no seu ambiente.")

def extrair_texto_docx(arquivo_docx):
    """Lê arquivos Word e extrai o texto de forma estruturada."""
    doc = docx.Document(arquivo_docx)
    return "\n".join([para.text for para in doc.paragraphs])

# --- 4. SISTEMA DE NAVEGAÇÃO SUPERIOR (COMMAND CENTER) ---
st.markdown('<div style="text-align: center; font-weight: bold; color: #3b82f6; margin-top: 15px; font-size: 14px; letter-spacing: 2px; text-transform: uppercase;">TechnoBolt AI Command Center</div>', unsafe_allow_html=True)

menu_opcoes = [
    "🏠 Dashboard Inicial", 
    "📁 Analisador de Documentos & Contratos",
    "✉️ Gerador de Email Inteligente", 
    "🧠 Briefing Negocial Estratégico", 
    "📝 Analista de Atas de Governança",
    "📈 Inteligência Competitiva & Churn"
]
menu_selecionado = st.selectbox("Selecione o Módulo Corporativo", menu_opcoes, label_visibility="collapsed")
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
        st.markdown("### ✉️ Comunicação\nCrie e-mails executivos de alto nível em segundos, ajustando cargo e tom para garantir a melhor percepção do destinatário.")
    with col3:
        st.markdown("### 📊 Inteligência\nMonitore movimentos da concorrência e utilize IA para prever riscos de cancelamento de contratos através do sentimento do cliente.")
    
    st.markdown("---")
    st.markdown("""
    ### 🛠️ Guia de Utilização Profissional:
    1. **Navegação:** Utilize o menu suspenso central no topo para navegar entre os 6 módulos de inteligência.
    2. **Análise de Arquivos:** No módulo de documentos, você pode subir arquivos **PDF, DOCX ou TXT**. O sistema extrai os dados e processa o resumo executivo.
    3. **Briefing Negocial:** Ideal para reuniões rápidas. Informe a empresa e o setor para receber um panorama de mercado 2025.
    4. **Inteligência:** Use a aba de Churn para colar e-mails de clientes insatisfeitos e receber orientações de como reverter a situação.
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
                        conteudo_ia = [f"Analise o seguinte conteúdo extraído de um documento Word:\n\n{texto_w}"]
                    else:
                        conteudo_ia = [arquivo.read().decode("utf-8")]

                    prompt_doc = """
                    Atue como um Consultor Estratégico Sênior (ex-McKinsey). Analise o documento e gere um relatório executivo estruturado:
                    - **RESUMO EXECUTIVO:** O que é o documento em linguagem simples para diretoria.
                    - **ANÁLISE DE IMPACTO:** Traduza termos técnicos para RISCO, CUSTO ESTIMADO e OPORTUNIDADES.
                    - **PONTOS CRÍTICOS:** O que o gestor NÃO pode ignorar sob nenhuma hipótese.
                    - **PLANO DE AÇÃO:** 3 passos imediatos sugeridos com base em boas práticas globais.
                    - **SUGESTÃO DE RESPOSTA:** Um rascunho de e-mail ou feedback formal que o gestor pode utilizar para responder a este documento.
                    """
                    response = model.generate_content([prompt_doc] + conteudo_ia)
                    st.markdown("---")
                    st.markdown("### 📊 Relatório de Inteligência Gerado")
                    st.markdown(response.text)
                    st.download_button("📥 Exportar Relatório para MD", response.text, file_name="analise_executiva_technobolt.md")
                except Exception as e: st.error(f"Erro no processamento: {e}")

# --- TELA: GERADOR DE EMAIL ---
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1><p>Comunicação executiva precisa e estratégica</p></div>', unsafe_allow_html=True)
    col_em1, col_em2 = st.columns(2)
    with col_em1: cargo_user = st.text_input("Seu Cargo:", placeholder="Ex: Diretor de Tecnologia")
    with col_em2: dest_user = st.text_input("Destinatário:", placeholder="Ex: Investidores da Rodada B")
    objetivo_msg = st.text_area("Objetivo Central da Mensagem:", placeholder="Ex: Explicar o impacto da nova regulamentação no cronograma do projeto...")
    tom_formalidade = st.select_slider("Grau de Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    
    if st.button("🚀 GERAR COMUNICAÇÃO DE ALTO IMPACTO"):
        with st.spinner("IA redigindo conteúdo com tom profissional..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_email = f"Como {cargo_user}, escreva um e-mail para {dest_user} focado em {objetivo_msg}. Use tom {tom_formalidade}. Seja persuasivo, direto e mantenha o padrão de alta gestão."
                res = model.generate_content(prompt_email)
                st.text_area("Cópia disponível para uso imediato:", res.text, height=450)
            except Exception as e: st.error(f"Erro na geração do e-mail: {e}")

# --- TELA: BRIEFING NEGOCIAL ---
elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Negocial Estratégico</h1><p>Radar de mercado e monitoramento de tendências de setor</p></div>', unsafe_allow_html=True)
    col_b1, col_b2 = st.columns(2)
    with col_b1: empresa_nome = st.text_input("Empresa Alvo:")
    with col_b2: setor_nome = st.text_input("Setor de Atuação:")
    
    tags_ativas = st.multiselect("Filtros de Inteligência (Radar):", options=st.session_state.tags, default=["Novas Leis", "Concorrência"])
    
    nova_tag_req = st.text_input("➕ Adicionar Novo Filtro ao Radar:")
    if nova_tag_req and nova_tag_req not in st.session_state.tags:
        st.session_state.tags.append(nova_tag_req)
        st.rerun()
    
    if st.button("⚡ ESCANEAR MERCADO E TENDÊNCIAS"):
        with st.spinner("Cruzando notícias e dados estratégicos de 2025..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_briefing = f"Gere um briefing executivo para a empresa {empresa_nome} no setor {setor_nome} focado nos pilares: {tags_ativas}."
                res_brief = model.generate_content(prompt_briefing)
                st.markdown(res_brief.text)
            except Exception as e: st.error(f"Erro na análise de mercado: {e}")

# --- TELA: ANALISTA DE ATAS ---
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas de Governança</h1><p>Formalização de reuniões a partir de anotações brutas</p></div>', unsafe_allow_html=True)
    notas_reuniao = st.text_area("Insira as notas brutas (quem estava presente, o que foi decidido, próximos passos):", height=300)
    if st.button("📝 GERAR ATA OFICIAL"):
        with st.spinner("IA estruturando documento de conformidade..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_ata = f"Aja como um Secretário de Governança Corporativa. Transforme estas notas em uma ata formal, estruturada com cabeçalho, pauta, deliberações e tabela de planos de ação: {notas_reuniao}"
                res_ata = model.generate_content(prompt_ata)
                st.markdown(res_ata.text)
            except Exception as e: st.error(f"Erro na ata: {e}")

# --- TELA: INTELIGÊNCIA COMPETITIVA ---
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência Competitiva & Churn</h1><p>Análise de rivais e proteção de base de clientes</p></div>', unsafe_allow_html=True)
    tab_rival, tab_churn = st.tabs(["🔍 Radar de Concorrência", "⚠️ Previsão de Perda (Churn)"])
    
    with tab_rival:
        nome_concorrente = st.text_input("Nome da Empresa Rival:")
        if st.button("📡 ANALISAR ESTRATÉGIA DO CONCORRENTE"):
            with st.spinner("Analisando brechas comerciais..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    res_riv = model.generate_content(f"Analise a estratégia pública recente da {nome_concorrente} e identifique brechas onde podemos atuar.")
                    st.markdown(res_riv.text)
                except Exception as e: st.error(e)
                
    with tab_churn:
        texto_feedback = st.text_area("Feedback crítico ou e-mail de reclamação do cliente:")
        if st.button("🧠 AVALIAR RISCO E AÇÃO DE RETENÇÃO"):
            with st.spinner("Analisando sentimento e probabilidade de perda..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    prompt_churn = f"Com base neste texto de cliente, avalie o risco de churn (0-100%). Explique os gatilhos de insatisfação e sugira uma ação imediata de retenção para o gestor: {texto_feedback}"
                    res_ch = model.generate_content(prompt_churn)
                    st.markdown(res_ch.text)
                except Exception as e: st.error(e)

# --- RODAPÉ CORPORATIVO ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Enterprise Strategic Edition v4.5 (Full Code)")