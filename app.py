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

# --- 2. CSS ULTRA FORÇADO (BLINDAGEM CONTRA PARTES BRANCAS) ---
st.markdown("""
<style>
    /* FUNDO ESCURO GLOBAL ABSOLUTO */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
    .stApp, [data-testid="stMain"], [data-testid="stVerticalBlock"],
    [data-testid="stMarkdownContainer"], .main {
        background-color: #0d1117 !important;
        color: #ffffff !important;
    }

    /* REMOÇÃO DE ELEMENTOS NATIVOS */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* FORÇA TODAS AS FONTES E LABELS PARA BRANCO */
    h1, h2, h3, h4, h5, h6, p, label, span, div, .stMarkdown, 
    [data-testid="stWidgetLabel"] p, [data-testid="stMarkdownContainer"] p,
    [data-testid="stHeader"], .stSelectbox label, .stTextInput label { 
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

    /* CUSTOMIZAÇÃO DE INPUTS, SELECTBOX E TEXTAREAS */
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

    /* BOTÕES EXECUTIVOS PREMIUM */
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

    /* TABS E TAGS PERSONALIZADAS */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: 600; }
    span[data-baseweb="tag"] { background-color: #1d4ed8 !important; color: #ffffff !important; border-radius: 5px; }
    
    /* CORREÇÃO DO SLIDER */
    .stSlider label, .stSlider span { color: #ffffff !important; }
    
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
    """Extração profunda de texto para suporte a Microsoft Word."""
    doc = docx.Document(arquivo_docx)
    return "\n".join([para.text for para in doc.paragraphs])

# --- 4. SISTEMA DE NAVEGAÇÃO SUPERIOR ---
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

# --- 5. GESTÃO DE ESTADO (MEMÓRIA DE TAGS) ---
if 'tags' not in st.session_state:
    st.session_state.tags = ["Novas Leis", "Concorrência", "Inovação Tech", "Cenário Macro", "ESG"]

# --- 6. TELAS DETALHADAS ---

# --- TELA: DASHBOARD ---
if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #9ca3af !important; font-size: 18px;'>Plataforma Unificada de Inteligência Corporativa Sênior.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📄 Documentos\nAnálise técnica traduzida para visão de gestão, riscos e custos.")
    with col2:
        st.markdown("### ✉️ Comunicação\nRedação de e-mails executivos com precisão tonal e estratégica.")
    with col3:
        st.markdown("### 📊 Inteligência\nMonitoramento de mercado, rivais e prevenção de perda de clientes.")
    
    st.markdown("---")
    st.markdown("""
    **Como utilizar este Hub de Inteligência:**
    1. **Navegação:** Utilize o menu suspenso no topo para alternar entre as ferramentas.
    2. **Analisador:** Faça upload de relatórios ou contratos para obter um resumo executivo "McKinsey Style".
    3. **Briefing:** Escaneie tendências de mercado para empresas e setores específicos.
    4. **Inteligência:** Analise a saúde da sua carteira através do monitoramento de sentimentos e Churn.
    """)

# --- TELA: ANALISADOR DE DOCUMENTOS ---
elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos & Tradutor de Gestão</h1><p>Processamento inteligente para PDF, DOCX e TXT</p></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Suba um relatório técnico, contrato ou proposta comercial:", type=["pdf", "docx", "txt"])
    
    if arquivo:
        if st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
            with st.spinner("Gemini 3 Flash analisando complexidade técnica e extraindo insights..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    
                    # Lógica de extração baseada no tipo de arquivo para evitar Erro 400
                    if arquivo.type == "application/pdf":
                        conteudo_ia = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        texto = extrair_texto_docx(arquivo)
                        conteudo_ia = [f"Analise este conteúdo extraído de um arquivo Word:\n\n{texto}"]
                    else:
                        conteudo_ia = [arquivo.read().decode("utf-8")]

                    prompt = """
                    Você é um Consultor Estratégico Sênior. Analise o documento em anexo e gere um relatório executivo de alto nível:
                    - **RESUMO EXECUTIVO:** Do que se trata este documento de forma concisa.
                    - **ANÁLISE DE IMPACTO:** Traduza termos técnicos para Impactos de Negócio (Risco, Custo e Oportunidade).
                    - **PONTOS CRÍTICOS:** O que o gestor NÃO pode ignorar sob nenhuma hipótese.
                    - **PLANO DE AÇÃO:** 3 passos imediatos sugeridos com base em boas práticas de mercado.
                    - **SUGESTÃO DE RESPOSTA:** Um rascunho de e-mail ou feedback formal que o gestor pode utilizar.
                    """
                    response = model.generate_content([prompt] + conteudo_ia)
                    st.markdown("---")
                    st.markdown("### 📊 Resultado da Análise")
                    st.markdown(response.text)
                    st.download_button("📥 Baixar Relatório Estratégico (.md)", response.text, file_name="analise_technobolt.md")
                except Exception as e: st.error(f"Erro no processamento do arquivo: {e}")

# --- TELA: EMAIL ---
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1><p>Comunicação executiva de alto impacto e tom ajustável</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: cargo = st.text_input("Seu Cargo:", placeholder="Ex: Diretor de Operações")
    with c2: dest = st.text_input("Destinatário:", placeholder="Ex: CEO da Holding")
    obj = st.text_area("Objetivo Central da Mensagem:", placeholder="Ex: Comunicar o atingimento das metas do Q3 e solicitar aprovação para...")
    formalidade = st.select_slider("Grau de Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    
    if st.button("🚀 GERAR COMUNICAÇÃO PROFISSIONAL"):
        with st.spinner("IA redigindo conteúdo estratégico..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_e = f"Como {cargo}, escreva um e-mail para {dest} focado em {obj}. Utilize um tom {formalidade}. Seja persuasivo e profissional."
                res = model.generate_content(prompt_e)
                st.text_area("Cópia disponível para uso:", res.text, height=400)
            except Exception as e: st.error(f"Erro na geração do e-mail: {e}")

# --- TELA: BRIEFING ---
elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Negocial Estratégico</h1><p>Radar de mercado e monitoramento de tendências</p></div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a: emp = st.text_input("Nome da Empresa Alvo:")
    with col_b: setor = st.text_input("Setor de Atuação:")
    
    tags_s = st.multiselect("Filtros de Inteligência (Radar):", options=st.session_state.tags, default=["Novas Leis"])
    
    nova_tag = st.text_input("➕ Adicionar Novo Filtro ao Radar:")
    if nova_tag and nova_tag not in st.session_state.tags:
        st.session_state.tags.append(nova_tag)
        st.rerun()
    
    if st.button("⚡ ESCANEAR MERCADO E TENDÊNCIAS"):
        with st.spinner("Cruzando dados globais e tendências de mercado..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_b = f"Gere um briefing executivo para a empresa {emp} no setor {setor} focado nos pilares: {tags_s}."
                res = model.generate_content(prompt_b)
                st.markdown(res.text)
            except Exception as e: st.error(f"Erro no briefing: {e}")

# --- TELA: ATAS ---
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas de Governança</h1><p>Transformação de notas em documentos oficiais</p></div>', unsafe_allow_html=True)
    txt_ata = st.text_area("Insira as notas brutas da reunião (Decisões, participantes, prazos):", height=300)
    if st.button("📝 FORMALIZAR DOCUMENTO"):
        with st.spinner("Estruturando ata de diretoria..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                res = model.generate_content(f"Transforme estas anotações em uma ata de governança formal e estruturada: {txt_ata}")
                st.markdown(res.text)
            except Exception as e: st.error(e)

# --- TELA: INTELIGÊNCIA COMPETITIVA ---
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência Competitiva & Churn</h1><p>Análise de rivais e proteção de base de clientes</p></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Radar de Rivais", "⚠️ Previsão de Perda (Churn)"])
    
    with t1:
        rival_n = st.text_input("Nome da Empresa Concorrente:")
        if st.button("📡 ANALISAR MOVIMENTAÇÕES RIVAIS"):
            with st.spinner("Analisando brechas e estratégias do concorrente..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    res = model.generate_content(f"Analise a estratégia pública recente da {rival_n} e identifique brechas de mercado.")
                    st.markdown(res.text)
                except Exception as e: st.error(e)
                
    with t2:
        feed_c = st.text_area("Insira o feedback do cliente ou histórico de interação recente:")
        if st.button("🧠 AVALIAR RISCO DE SAÍDA"):
            with st.spinner("Analisando sentimento e probabilidade de Churn..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    res = model.generate_content(f"Com base neste texto de cliente, avalie o risco de perda (0 a 100%) e sugira uma ação de retenção: {feed_c}")
                    st.markdown(res.text)
                except Exception as e: st.error(e)

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Enterprise Edition v4.0 (Strategic Full Code)")