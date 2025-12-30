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

# --- 2. CSS ULTRA FORÇADO (BLINDAGEM TOTAL E CORREÇÕES VISUAIS) ---
st.markdown("""
<style>
    /* 1. FUNDO ESCURO GLOBAL ABSOLUTO EM TODOS OS NÍVEIS */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
    .stApp, [data-testid="stMain"], [data-testid="stVerticalBlock"],
    [data-testid="stMarkdownContainer"], .main, [data-testid="stBlock"] {
        background-color: #0d1117 !important;
        color: #ffffff !important;
    }

    /* 2. REMOÇÃO DE ELEMENTOS NATIVOS E CABEÇALHOS */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* 3. FORÇA TODAS AS FONTES PARA BRANCO (ESTADO ATIVO E INATIVO) */
    h1, h2, h3, h4, h5, h6, p, label, span, div, .stMarkdown, 
    [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p,
    [data-testid="stHeader"], .stSelectbox label, .stTextInput label,
    .stTextArea label, [data-testid="stMetricValue"] { 
        color: #ffffff !important; 
    }

    /* 4. TÍTULO E CABEÇALHOS CORPORATIVOS CUSTOMIZADOS */
    .main-title { 
        font-size: 38px; font-weight: 900; text-align: center; 
        margin-top: 10px; margin-bottom: 5px; color: #ffffff !important;
        letter-spacing: -1.5px;
    }
    .product-header { 
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%); 
        padding: 30px; border-radius: 15px; margin-bottom: 30px; 
        text-align: center; border: 1px solid #374151;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }

    /* 5. CUSTOMIZAÇÃO DA LISTA SUSPENSA (SELECTBOX) - CORREÇÃO DE FUNDO BRANCO */
    div[data-baseweb="select"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 10px;
    }
    
    /* Fundo da lista aberta e itens */
    ul[role="listbox"] {
        background-color: #161b22 !important;
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

    /* 6. INPUTS E TEXTAREAS (EVITA BORDAS CLARAS) */
    .stTextInput input, .stTextArea textarea {
        background-color: #0d1117 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }

    /* 7. BOTÕES EXECUTIVOS PREMIUM (REMOÇÃO DE FAIXAS PRETAS) */
    .stButton > button { 
        width: 100%; border-radius: 12px; height: 4em; font-weight: bold; 
        background-color: #238636 !important; color: #ffffff !important; 
        border: none !important; outline: none !important;
        box-shadow: none !important; text-transform: uppercase; 
        letter-spacing: 1px; transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #2ea043 !important;
        transform: scale(1.01);
        border: none !important;
    }
    .stButton > button:active, .stButton > button:focus {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /* 8. ÁREA DE UPLOAD E TABS */
    [data-testid="stFileUploader"] section {
        background-color: #161b22 !important;
        border: 2px dashed #30363d !important;
        border-radius: 15px;
        padding: 20px;
        color: #ffffff !important;
    }
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: 600; }
    
    /* 9. SLIDERS E TAGS */
    .stSlider label, .stSlider span { color: #ffffff !important; }
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
    st.error("⚠️ Configuração Pendente: GEMINI_API_KEY não encontrada nas variáveis de ambiente.")

def extrair_texto_docx(arquivo_docx):
    """Extração profunda de texto para suporte total a documentos Microsoft Word."""
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

# --- 6. TELAS DETALHADAS ---

# --- TELA: DASHBOARD INICIAL ---
if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #9ca3af !important; font-size: 18px;'>Plataforma Unificada de Inteligência Corporativa Sênior.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📄 Documentos\nTransforme relatórios técnicos densos em resumos executivos focados em Riscos, Custos e Ações.")
    with col2:
        st.markdown("### ✉️ Comunicação\nRedação de e-mails executivos de alto impacto com ajuste fino de cargo, destinatário e tom.")
    with col3:
        st.markdown("### 📊 Inteligência\nMonitoramento competitivo de rivais e análise de sentimento para prevenção de perda de clientes.")
    
    st.markdown("---")
    st.markdown("""
    ### 🛠️ Orientações de Uso:
    1. **Navegação:** Utilize o menu suspenso no topo para alternar instantaneamente entre os módulos.
    2. **Analisador:** Faça upload de arquivos PDF ou Word para extrair insights estratégicos imediatos.
    3. **Briefing:** Configure radares personalizados para escanear mercados, setores e empresas específicas.
    4. **Governança:** Utilize o Analista de Atas para formalizar reuniões complexas a partir de notas simples.
    5. **Estratégia:** Acesse o radar competitivo para identificar brechas em seus principais concorrentes.
    """)

# --- TELA: ANALISADOR DE DOCUMENTOS ---
elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos & Tradutor de Gestão</h1><p>Processamento inteligente para PDF, DOCX (Word) e TXT</p></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Arraste ou selecione seu relatório técnico ou contrato:", type=["pdf", "docx", "txt"])
    
    if arquivo:
        if st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
            with st.spinner("Gemini 3 Flash processando inteligência técnica e traduzindo para gestão..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    
                    # Lógica de processamento híbrida para evitar erros de MIME type
                    if arquivo.type == "application/pdf":
                        conteudo_ia = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        texto_word = extrair_texto_docx(arquivo)
                        conteudo_ia = [f"Analise estrategicamente este conteúdo extraído de um documento Word:\n\n{texto_word}"]
                    else:
                        conteudo_ia = [arquivo.read().decode("utf-8")]

                    prompt_doc = """
                    Você é um Consultor de Estratégia Sênior (ex-McKinsey). Analise o documento em anexo e produza um relatório executivo:
                    - **RESUMO EXECUTIVO:** O que é o documento em linguagem simples e direta.
                    - **ANÁLISE DE IMPACTO:** Traduza os dados técnicos para RISCO, CUSTO ESTIMADO e OPORTUNIDADES.
                    - **PONTOS CRÍTICOS:** O que o gestor NÃO pode ignorar sob nenhuma hipótese.
                    - **PLANO DE AÇÃO:** 3 passos imediatos sugeridos baseados em boas práticas globais.
                    - **SUGESTÃO DE RESPOSTA:** Um rascunho de e-mail ou feedback formal para o autor do documento.
                    """
                    response = model.generate_content([prompt_doc] + conteudo_ia)
                    st.markdown("---")
                    st.markdown("### 📊 Resultado da Análise Corporativa")
                    st.markdown(response.text)
                    st.download_button("📥 Baixar Relatório (.md)", response.text, file_name="analise_technobolt.md")
                except Exception as e: st.error(f"Erro no processamento do arquivo: {e}")

# --- TELA: GERADOR DE EMAIL ---
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1><p>Comunicação executiva de alto impacto e tom ajustável</p></div>', unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)
    with col_e1: cargo = st.text_input("Seu Cargo:", placeholder="Ex: Diretor de Operações")
    with col_e2: dest = st.text_input("Destinatário:", placeholder="Ex: CEO da Holding")
    obj = st.text_area("Objetivo Central da Mensagem:", placeholder="Ex: Justificar o aumento de orçamento para o projeto de IA...")
    formalidade = st.select_slider("Grau de Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    
    if st.button("🚀 GERAR COMUNICAÇÃO PROFISSIONAL"):
        with st.spinner("IA redigindo conteúdo estratégico..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_email = f"Como {cargo}, escreva um e-mail profissional para {dest} focado em: {obj}. Utilize um tom {formalidade}. Seja conciso, persuasivo e direto ao ponto."
                res = model.generate_content(prompt_email)
                st.text_area("Rascunho gerado (copie para seu e-mail):", res.text, height=450)
            except Exception as e: st.error(f"Erro na geração: {e}")

# --- TELA: BRIEFING NEGOCIAL ---
elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Negocial Estratégico</h1><p>Radar de mercado e monitoramento ativo de tendências</p></div>', unsafe_allow_html=True)
    c_b1, c_b2 = st.columns(2)
    with c_b1: empresa_alvo = st.text_input("Nome da Empresa Alvo:")
    with c_b2: setor_atuacao = st.text_input("Setor de Atuação:")
    
    tags_selecionadas = st.multiselect("Pilares do Radar de Inteligência:", options=st.session_state.tags, default=["Novas Leis", "Concorrência"])
    
    nova_tag_input = st.text_input("➕ Adicionar Novo Filtro ao seu Radar Personalizado:")
    if nova_tag_input and nova_tag_input not in st.session_state.tags:
        st.session_state.tags.append(nova_tag_input)
        st.rerun()
    
    if st.button("⚡ ESCANEAR MERCADO E TENDÊNCIAS"):
        with st.spinner("Analisando notícias globais e tendências de setor 2025..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_briefing = f"Gere um briefing executivo para a empresa {empresa_alvo} no setor {setor_atuacao} focando nos seguintes pilares estratégicos: {tags_selecionadas}."
                res = model.generate_content(prompt_briefing)
                st.markdown(res.text)
            except Exception as e: st.error(f"Erro no briefing: {e}")

# --- TELA: ANALISTA DE ATAS ---
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas de Governança</h1><p>Transformação instantânea de notas em documentos de conformidade</p></div>', unsafe_allow_html=True)
    texto_notas = st.text_area("Insira as notas brutas da reunião (Participantes, tópicos e decisões):", height=300)
    if st.button("📝 FORMALIZAR DOCUMENTO OFICIAL"):
        with st.spinner("Estruturando ata de diretoria em formato profissional..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                res_ata = model.generate_content(f"Aja como um Secretário de Governança. Transforme as seguintes anotações em uma ata de diretoria formal, estruturada com pauta, deliberações e prazos: {texto_notas}")
                st.markdown(res_ata.text)
            except Exception as e: st.error(f"Erro na ata: {e}")

# --- TELA: INTELIGÊNCIA COMPETITIVA ---
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência Competitiva & Churn</h1><p>Proteção de base e análise estratégica de rivais</p></div>', unsafe_allow_html=True)
    tab_rival, tab_churn = st.tabs(["🔍 Radar de Rivais", "⚠️ Previsão de Perda (Churn)"])
    
    with tab_rival:
        nome_rival = st.text_input("Nome da Empresa Concorrente:")
        if st.button("📡 ANALISAR MOVIMENTAÇÕES DO RIVAL"):
            with st.spinner("Cruzando dados de mercado e identificando vulnerabilidades..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    res_rival = model.generate_content(f"Analise a estratégia pública recente da empresa {nome_rival}. Identifique brechas competitivas e sugira contra-movimentos estratégicos.")
                    st.markdown(res_rival.text)
                except Exception as e: st.error(f"Erro na análise: {e}")
                
    with tab_churn:
        feedback_texto = st.text_area("Insira o feedback crítico do cliente ou histórico de interação recente:")
        if st.button("🧠 AVALIAR RISCO E SUGERIR RETENÇÃO"):
            with st.spinner("Analisando sentimento e probabilidade de Churn..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    res_churn = model.generate_content(f"Com base neste feedback de cliente, avalie o risco de perda em uma escala de 0 a 100%. Explique os motivos e sugira uma estratégia imediata de retenção para o gestor de contas: {feedback_texto}")
                    st.markdown(res_churn.text)
                except Exception as e: st.error(f"Erro na previsão: {e}")

# --- RODAPÉ CORPORATIVO ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Enterprise Strategic Edition v4.3 (Full Code)")