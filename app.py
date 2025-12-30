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

# --- 2. CSS ULTRA-BLINDADO (DARK MODE TOTAL & CORREÇÃO VISUAL DEFINITIVA) ---
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

    /* 3. FORÇA FONTES BRANCAS EM TUDO (MESMO DENTRO DE INPUTS E LISTAS) */
    * { 
        color: #ffffff !important; 
        -webkit-text-fill-color: #ffffff !important;
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

    /* 5. CORREÇÃO DA BARRA DE SERVIÇOS (SELECTBOX) E MENU SUSPENSO FLUTUANTE */
    /* Garante que o fundo da barra e da lista aberta nunca fiquem brancos */
    div[data-baseweb="select"], div[data-baseweb="popover"], ul[role="listbox"], 
    [data-baseweb="popover"] *, [data-baseweb="select"] * {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
    }
    
    /* Hover e Seleção na lista para visibilidade executiva */
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }

    /* 6. CORREÇÃO DOS BOTÕES (ELIMINA FAIXAS PRETAS E BORDAS RESIDUAIS) */
    .stButton > button { 
        width: 100%; border-radius: 15px; height: 4.2em; font-weight: bold; 
        background-color: #238636 !important; /* Verde Corporativo */
        color: #ffffff !important; 
        border: none !important;
        outline: none !important; /* Remove a faixa preta de foco do navegador */
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        transition: all 0.3s ease-in-out;
    }
    
    /* Mantém o botão verde em todos os estados de interação */
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

    /* 7. CUSTOMIZAÇÃO DE INPUTS E TEXTAREAS (TEXTO SEMPRE CLARO) */
    .stTextInput input, .stTextArea textarea {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* 8. TABS, SLIDERS E ÁREA DE UPLOAD */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: 700; }
    
    [data-testid="stFileUploader"] section {
        background-color: #161b22 !important;
        border: 2px dashed #30363d !important;
        border-radius: 15px;
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
    st.error("⚠️ Configuração Pendente: GEMINI_API_KEY não encontrada.")

def extrair_texto_docx(arquivo_docx):
    """Lê arquivos Word (.docx) e extrai o texto de forma estruturada."""
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
# Seleção centralizada que controla o Hub
menu_selecionado = st.selectbox("Selecione o Módulo Ativo", menu_opcoes, label_visibility="collapsed")
st.markdown("<hr>", unsafe_allow_html=True)

# --- 5. GESTÃO DE ESTADO (MEMÓRIA DE TAGS E SESSÃO) ---
if 'tags' not in st.session_state:
    st.session_state.tags = ["Novas Leis", "Concorrência", "Inovação Tech", "Cenário Macro", "ESG"]

# --- 6. TELAS DO HUB ---

# --- TELA: DASHBOARD INICIAL ---
if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #9ca3af !important; font-size: 18px;'>Plataforma Unificada de Inteligência Corporativa para Alta Gestão.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📄 Documentos\nTraduz relatórios técnicos para uma visão executiva focada em Riscos, Custos e Ações.")
    with col2:
        st.markdown("### ✉️ Comunicação\nRedação de e-mails de alto impacto com ajuste de cargo e tom estratégico.")
    with col3:
        st.markdown("### 📊 Inteligência\nMonitoramento de mercado e análise de sentimento para retenção de clientes.")
    
    st.markdown("---")
    st.markdown("""
    ### 🛠️ Guia de Operação:
    1. **Navegação:** Utilize o menu suspenso no topo para alternar entre as ferramentas.
    2. **Analisador:** Faça upload de arquivos **PDF, DOCX ou TXT** para extrair insights estratégicos.
    3. **Briefing:** Ideal para panoramas rápidos de mercado baseados em empresa e setor.
    4. **Inteligência:** Use a aba de Churn para avaliar o risco de perda baseado no feedback do cliente.
    """)

# --- TELA: ANALISADOR DE DOCUMENTOS ---
elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos & Tradutor de Gestão</h1><p>Processamento inteligente para PDF, DOCX (Word) e TXT</p></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Suba o documento técnico ou contrato comercial:", type=["pdf", "docx", "txt"])
    
    if arquivo:
        if st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
            with st.spinner("IA processando inteligência técnica e traduzindo para gestão..."):
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
                    Atue como um Consultor de Estratégia Sênior. Analise o documento e gere um relatório executivo:
                    - **RESUMO EXECUTIVO:** O que é o documento em linguagem executiva.
                    - **ANÁLISE DE IMPACTO:** Traduza para RISCO, CUSTO ESTIMADO e OPORTUNIDADES.
                    - **PONTOS CRÍTICOS:** O que o gestor NÃO pode ignorar.
                    - **PLANO DE AÇÃO:** 3 passos imediatos sugeridos.
                    - **SUGESTÃO DE RESPOSTA:** Um rascunho de e-mail formal de feedback.
                    """
                    response = model.generate_content([prompt_doc] + conteudo_ia)
                    st.markdown("---")
                    st.markdown("### 📊 Resultado da Análise")
                    st.markdown(response.text)
                    st.download_button("📥 Baixar Relatório (.md)", response.text, file_name="analise_technobolt.md")
                except Exception as e: st.error(f"Erro no processamento: {e}")

# --- TELA: GERADOR DE EMAIL ---
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1><p>Redação executiva veloz e estratégica</p></div>', unsafe_allow_html=True)
    col_e1, col_e2 = st.columns(2)
    with col_e1: cargo = st.text_input("Seu Cargo:", placeholder="Ex: Diretor de Operações")
    with col_e2: dest = st.text_input("Destinatário:", placeholder="Ex: CEO da Holding")
    obj = st.text_area("Objetivo Central da Mensagem:", placeholder="Ex: Justificar o aumento de orçamento para o projeto X...")
    formalidade = st.select_slider("Grau de Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    
    if st.button("🚀 GERAR COMUNICAÇÃO PROFISSIONAL"):
        with st.spinner("IA redigindo conteúdo profissional..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_email = f"Como {cargo}, escreva um e-mail para {dest} focado em {obj}. Tom {formalidade}. Seja conciso e direto."
                res = model.generate_content(prompt_email)
                st.text_area("Rascunho disponível:", res.text, height=450)
            except Exception as e: st.error(f"Erro na geração: {e}")

# --- TELA: BRIEFING NEGOCIAL ---
elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Negocial Estratégico</h1><p>Radar de mercado em tempo real</p></div>', unsafe_allow_html=True)
    c_b1, c_b2 = st.columns(2)
    with c_b1: empresa = st.text_input("Nome da Empresa Alvo:")
    with c_b2: setor = st.text_input("Setor de Atuação:")
    
    tags_s = st.multiselect("Filtros do Radar:", options=st.session_state.tags, default=["Novas Leis"])
    
    nova_tag_input = st.text_input("➕ Adicionar Novo Filtro ao Radar:")
    if nova_tag_input and nova_tag_input not in st.session_state.tags:
        st.session_state.tags.append(nova_tag_input)
        st.rerun()
    
    if st.button("⚡ ESCANEAR MERCADO"):
        with st.spinner("Analisando notícias e tendências..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                prompt_b = f"Gere briefing executivo para {empresa} no setor {setor} focado em {tags_s}."
                res = model.generate_content(prompt_b)
                st.markdown(res.text)
            except Exception as e: st.error(f"Erro: {e}")

# --- TELA: ANALISTA DE ATAS ---
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas de Governança</h1><p>Formalização ágil de deliberações</p></div>', unsafe_allow_html=True)
    txt_ata = st.text_area("Notas brutas da reunião (Participantes, pautas e decisões):", height=300)
    if st.button("📝 FORMALIZAR DOCUMENTO"):
        with st.spinner("Estruturando ata de diretoria..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                res = model.generate_content(f"Transforme em ata formal de diretoria: {txt_ata}")
                st.markdown(res.text)
            except Exception as e: st.error(e)

# --- TELA: INTELIGÊNCIA COMPETITIVA ---
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência Competitiva & Churn</h1><p>Análise de rivais e proteção de base de clientes</p></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Radar de Rivais", "⚠️ Risco de Churn"])
    
    with t1:
        rival_n = st.text_input("Nome do Concorrente:")
        if st.button("📡 ANALISAR MOVIMENTAÇÕES"):
            with st.spinner("Cruzando dados de mercado..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    res = model.generate_content(f"Analise a estratégia da empresa {rival_n} e aponte brechas.")
                    st.markdown(res.text)
                except Exception as e: st.error(e)
                
    with t2:
        feed = st.text_area("Feedback do cliente:")
        if st.button("🧠 AVALIAR RISCO"):
            with st.spinner("Analisando sentimento..."):
                try:
                    model = genai.GenerativeModel(MODEL_NAME)
                    res = model.generate_content(f"Analise o risco de churn e sugira ação de retenção: {feed}")
                    st.markdown(res.text)
                except Exception as e: st.error(e)

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Enterprise Edition v5.0 Full Code")