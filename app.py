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

# --- 2. CSS PREMIUM GLASSMORPHISM (DARK MODE ABSOLUTO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');

    /* FUNDO ESCURO GLOBAL */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
    .stApp, [data-testid="stMain"], [data-testid="stVerticalBlock"] {
        background-color: #05070a !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* FORÇA FONTES BRANCAS EM TUDO */
    * { 
        color: #f8fafc !important; 
        -webkit-text-fill-color: #f8fafc !important;
    }

    /* HEADER CORPORATIVO COM GRADIENTE */
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

    /* MENU SELECTBOX - DROPDOWN DARK */
    div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(59, 130, 246, 0.5) !important;
        border-radius: 14px !important;
    }
    
    div[data-baseweb="popover"] > div, ul[role="listbox"] {
        background-color: #0f172a !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* BOTÃO "BROWSE FILES" CUSTOMIZADO */
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 25px !important;
        font-weight: 700 !important;
    }

    /* BOTÃO PRINCIPAL VERDE GLOSSY */
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

    /* INPUTS MODERNOS */
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        padding: 18px !important;
    }

    hr { border: 0.5px solid rgba(255, 255, 255, 0.1) !important; margin: 40px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE: CONFIGURAÇÃO DA API E MODELO ---
api_key = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "models/gemini-3-flash-preview"

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Erro: Chave de API não encontrada.")

def extrair_texto_docx(arquivo_docx):
    """Extração profunda de arquivos Microsoft Word."""
    doc = docx.Document(arquivo_docx)
    return "\n".join([para.text for para in doc.paragraphs])

# --- 4. NAVEGAÇÃO SUPERIOR ---
st.markdown('<div style="text-align: center; font-weight: 700; color: #94a3b8; margin-top: 20px; font-size: 12px; letter-spacing: 4px;">TECHNOBOLT COMMAND CENTER v7.1</div>', unsafe_allow_html=True)

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

# --- 5. GESTÃO DE ESTADO ---
if 'tags' not in st.session_state:
    st.session_state.tags = ["Novas Leis", "Concorrência", "Inovação Tech", "Cenário Macro", "ESG"]

# --- 6. TELAS DO HUB ---

# --- TELA: DASHBOARD ---
if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #64748b !important; font-size: 20px; margin-bottom: 40px;'>Inteligência Corporativa de Próxima Geração.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📄 Documentos\nResumos executivos focados em traduzir complexidade técnica para Riscos, Custos e Ações estratégicas.")
    with col2:
        st.markdown("### ✉️ Comunicação\nRedação de e-mails executivos de alto impacto com ajuste fino de tom profissional.")
    with col3:
        st.markdown("### 📊 Inteligência\nMonitoramento competitivo de rivais e análise de sentimento para prevenção de Churn.")
    
    st.markdown("---")
    st.markdown("""
    ### 🛠️ Guia de Operação Corporativa:
    1. **Navegação:** Utilize o menu suspenso no topo para alternar entre os 6 módulos.
    2. **Analisador:** Suba arquivos **PDF, DOCX ou TXT**. O sistema analisa sob a ótica de um Consultor Sênior.
    3. **Briefing:** Informe empresa e setor para receber um radar de mercado 2025 completo.
    4. **Atas:** Formalize reuniões a partir de anotações brutas de diretoria.
    5. **Churn:** Cole feedbacks críticos para receber estratégias imediatas de retenção de clientes.
    """)

# --- TELA: ANALISADOR DE DOCUMENTOS ---
elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos & Tradutor de Gestão</h1><p>Suporte para PDF, DOCX (Word) e TXT</p></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Suba o relatório técnico ou contrato:", type=["pdf", "docx", "txt"])
    
    if arquivo:
        if st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
            with st.spinner("IA processando inteligência técnica e traduzindo para visão executiva..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    if arquivo.type == "application/pdf":
                        conteudo_ia = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        texto_w = extrair_texto_docx(arquivo)
                        conteudo_ia = [f"Analise o seguinte conteúdo extraído de um Word:\n\n{texto_w}"]
                    else:
                        conteudo_ia = [arquivo.read().decode("utf-8")]

                    prompt_doc = """
                    Você é um Consultor de Estratégia Sênior (ex-McKinsey). Analise o documento em anexo e produza um relatório executivo:
                    - **RESUMO EXECUTIVO:** Do que se trata o documento em linguagem simples e executiva.
                    - **ANÁLISE DE IMPACTO:** Traduza termos técnicos para RISCO, CUSTO ESTIMADO e OPORTUNIDADES.
                    - **PONTOS CRÍTICOS:** O que o gestor NÃO pode ignorar sob nenhuma hipótese.
                    - **PLANO DE AÇÃO:** 3 passos imediatos sugeridos baseados em boas práticas de mercado.
                    - **SUGESTÃO DE RESPOSTA:** Um rascunho de e-mail formal para o autor do documento.
                    """
                    response = model.generate_content([prompt_doc] + conteudo_ia)
                    st.markdown("---")
                    st.markdown("### 📊 Resultado da Análise Gerencial")
                    st.markdown(response.text)
                except Exception as e: st.error(f"Erro: {e}")

# --- TELA: GERADOR DE EMAIL ---
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1><p>Redação executiva estratégica</p></div>', unsafe_allow_html=True)
    c_e1, c_e2 = st.columns(2)
    with c_e1: cargo = st.text_input("Seu Cargo:", placeholder="Ex: Diretor de Operações")
    with c_e2: dest = st.text_input("Destinatário:", placeholder="Ex: CEO da Holding")
    obj = st.text_area("Objetivo Central da Mensagem:", placeholder="Ex: Justificar o aumento de orçamento...")
    
    if st.button("🚀 GERAR COMUNICAÇÃO PROFISSIONAL"):
        with st.spinner("IA redigindo conteúdo profissional..."):
            model = genai.GenerativeModel(MODEL_NAME)
            prompt_email = f"Como {cargo}, escreva um e-mail para {dest} sobre {obj}. Use tom executivo, conciso e direto."
            res = model.generate_content(prompt_email)
            st.text_area("Rascunho:", res.text, height=450)

# --- TELA: BRIEFING NEGOCIAL ---
elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Negocial Estratégico</h1><p>Radar de mercado e tendências 2025</p></div>', unsafe_allow_html=True)
    c_b1, c_b2 = st.columns(2)
    with c_b1: empresa = st.text_input("Empresa Alvo:")
    with c_b2: setor = st.text_input("Setor:")
    
    tags_s = st.multiselect("Radar:", options=st.session_state.tags, default=["Novas Leis"])
    
    if st.button("⚡ ESCANEAR MERCADO"):
        with st.spinner("Analisando notícias globais..."):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Gere briefing executivo para {empresa} no setor {setor} sobre {tags_s}.")
            st.markdown(res.text)

# --- TELA: ANALISTA DE ATAS ---
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas</h1></div>', unsafe_allow_html=True)
    notas = st.text_area("Insira as notas brutas da reunião:", height=300)
    if st.button("📝 FORMALIZAR DOCUMENTO"):
        with st.spinner("Estruturando ata oficial..."):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Transforme estas notas em uma ata formal de diretoria: {notas}")
            st.markdown(res.text)

# --- TELA: INTELIGÊNCIA COMPETITIVA ---
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência Competitiva & Churn</h1></div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔍 Radar Rival", "⚠️ Churn"])
    with tab1:
        rival = st.text_input("Nome do Rival:")
        if st.button("📡 ANALISAR MOVIMENTAÇÕES"):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Analise a estratégia recente da empresa {rival} e identifique vulnerabilidades.")
            st.markdown(res.text)
    with tab2:
        feed = st.text_area("Feedback do cliente:")
        if st.button("🧠 AVALIAR RISCO"):
            model = genai.GenerativeModel(MODEL_NAME)
            res = model.generate_content(f"Avalie o risco de churn (0-100%) e sugira ação de retenção para: {feed}")
            st.markdown(res.text)

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Edição Integral v7.1")