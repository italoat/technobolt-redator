import streamlit as st
import google.generativeai as genai
import os
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="TechnoBolt IA - Hub Corporativo",
    page_icon="⚡",
    layout="wide"
)

# --- 2. CSS PARA DARK MODE TOTAL E UI EXECUTIVA ---
st.markdown("""
<style>
    /* OCULTA ELEMENTOS PADRÃO DO STREAMLIT */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* FUNDO ESCURO PROFUNDO */
    .stApp { 
        background-color: #0d1117 !important; 
        color: #ffffff !important; 
    }

    /* FORÇA TODAS AS FONTES PARA BRANCO */
    h1, h2, h3, h4, h5, h6, p, label, span, div, .stMarkdown, [data-testid="stWidgetLabel"] p { 
        color: #ffffff !important; 
    }

    /* TÍTULO PRINCIPAL */
    .main-title { 
        font-size: 36px; 
        font-weight: 800; 
        color: #ffffff !important; 
        text-align: center;
        margin-bottom: 5px;
    }

    /* CABEÇALHO DAS FERRAMENTAS */
    .product-header { 
        background: linear-gradient(90deg, #161b22, #0d1117); 
        color: #ffffff !important; 
        padding: 22px; 
        border-radius: 12px; 
        margin-bottom: 30px;
        text-align: center;
        border: 1px solid #30363d;
    }

    /* ESTILO DOS INPUTS, TEXTAREAS E SELECTBOXES */
    div[data-baseweb="select"], .stTextInput input, .stTextArea textarea {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }

    /* UPLOAD DE ARQUIVO DARK */
    [data-testid="stFileUploader"] section {
        background-color: #161b22 !important;
        border: 1px dashed #30363d !important;
        color: #ffffff !important;
    }

    /* BOTÕES EXECUTIVOS (VERDE SUCESSO) */
    .stButton > button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3.8em; 
        font-weight: bold; 
        background-color: #238636 !important; 
        color: #ffffff !important; 
        border: none;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #2ea043 !important;
        transform: translateY(-2px);
    }

    /* TABS E TAGS */
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; }
    span[data-baseweb="tag"] { background-color: #388bfd !important; color: #ffffff !important; }

    hr { border: 0.5px solid #30363d !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DA API ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 4. SISTEMA DE NAVEGAÇÃO SUPERIOR (IDEAL PARA IPHONE) ---
st.markdown('<div style="text-align: center; font-weight: bold; color: #58a6ff; margin-top: 15px; font-size: 13px;">CENTRAL DE INTELIGÊNCIA</div>', unsafe_allow_html=True)
menu_opcoes = [
    "🏠 Página Inicial", 
    "📁 Analisador de Documentos",
    "✉️ Gerador de Email Inteligente", 
    "🧠 Gerador de Briefing Negocial", 
    "📝 Analista de Atas de Governança",
    "📈 Inteligência Competitiva"
]
menu_selecionado = st.selectbox("Menu", menu_opcoes, label_visibility="collapsed")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 5. MEMÓRIA DE SESSÃO ---
if 'tags_disponiveis' not in st.session_state:
    st.session_state.tags_disponiveis = ["Novas Leis", "Concorrência", "Inovação", "Macroeconomia"]

# --- 6. TELAS DO HUB ---

# --- HOME ---
if "🏠 Página Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #8b949e !important;'>Transformando complexidade técnica em decisão executiva.</p>", unsafe_allow_html=True)
    
    st.markdown("""
    ### 🛠️ Módulos de Gestão:
    * **📁 Analisador de Documentos:** Traduza relatórios técnicos e contratos para linguagem de gestão.
    * **✉️ Gerador de Email:** Comunicação executiva rápida com ajuste de tom.
    * **🧠 Briefing Negocial:** Radar estratégico de mercado e tendências.
    * **📈 Inteligência Competitiva:** Análise de rivais e saúde de contratos (Churn).
    """)

# --- ANALISADOR DE DOCUMENTOS (NOVO) ---
elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header">📁 Analisador de Documentos & Tradutor de Gestão</div>', unsafe_allow_html=True)
    st.write("Transforme relatórios técnicos densos ou contratos em planos de ação estratégica.")
    
    arquivo = st.file_uploader("Anexe o documento (PDF, TXT ou DOCX):", type=["pdf", "txt", "docx"])
    
    if arquivo:
        if st.button("🔍 ANALISAR E TRADUZIR PARA GESTÃO"):
            with st.spinner("IA processando complexidade técnica e buscando boas práticas..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    conteudo = arquivo.read()
                    
                    prompt_executivo = f"""
                    Aja como um Consultor de Estratégia Sênior. 
                    Analise o documento técnico e produza um relatório para um Diretor/CEO.
                    
                    ESTRUTURA:
                    1. **Resumo Executivo (Simples):** Do que se trata o documento.
                    2. **Impacto para o Negócio:** Traduza termos técnicos para RISCO, CUSTO e OPORTUNIDADE.
                    3. **Pontos de Atenção:** O que o gestor deve focar agora.
                    4. **Plano de Ação:** 3 passos sugeridos com base em boas práticas globais.
                    5. **Sugestão de Resposta:** Redija um texto/e-mail para o gestor enviar como retorno a este documento.
                    """
                    
                    response = model.generate_content([prompt_executivo, {"mime_type": arquivo.type, "data": conteudo}])
                    st.markdown("---")
                    st.markdown(response.text)
                    st.download_button("📥 Baixar Relatório Estratégico", response.text, file_name="analise_technobolt.md")
                except Exception as e:
                    st.error(f"Erro na análise: {e}")

# --- GERADOR DE EMAIL ---
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header">✉️ Gerador de Email Inteligente</div>', unsafe_allow_html=True)
    cargo = st.text_input("Seu Cargo:")
    dest = st.text_input("Destinatário:")
    obj = st.text_area("Objetivo:")
    formalidade = st.select_slider("Formalidade:", ["Casual", "Cordial", "Executivo", "Rígido"], value="Executivo")
    if st.button("🚀 GERAR E-MAIL"):
        with st.spinner("Redigindo..."):
            model = genai.GenerativeModel("models/gemini-3-flash-preview")
            res = model.generate_content(f"Como {cargo}, escreva para {dest} sobre {obj}. Tom: {formalidade}.")
            st.text_area("Resultado:", res.text, height=400)

# --- BRIEFING NEGOCIAL ---
elif "🧠 Gerador de Briefing" in menu_selecionado:
    st.markdown('<div class="product-header">🧠 Gerador de Briefing Negocial</div>', unsafe_allow_html=True)
    empresa = st.text_input("Empresa:")
    setor = st.text_input("Setor:")
    tags = st.multiselect("Radar:", options=st.session_state.tags_disponiveis, default=["Novas Leis"])
    if st.button("⚡ ESCANEAR MERCADO"):
        with st.spinner("Analisando notícias..."):
            model = genai.GenerativeModel("models/gemini-3-flash-preview")
            res = model.generate_content(f"Gere briefing para {empresa} em {setor} sobre {tags}.")
            st.markdown(res.text)

# --- ANALISTA DE ATAS ---
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header">📝 Analista de Atas de Governança</div>', unsafe_allow_html=True)
    notas = st.text_area("Notas da reunião:", height=250)
    if st.button("📝 FORMALIZAR ATA"):
        with st.spinner("Formatando..."):
            model = genai.GenerativeModel("models/gemini-3-flash-preview")
            res = model.generate_content(f"Transforme em ata formal: {notas}")
            st.markdown(res.text)

# --- INTELIGÊNCIA COMPETITIVA ---
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header">📈 Inteligência Competitiva</div>', unsafe_allow_html=True)
    aba1, aba2 = st.tabs(["🔍 Radar de Concorrência", "❤️ Sentimento do Cliente"])
    with aba1:
        rival = st.text_input("Nome do Rival:")
        if st.button("📡 ANALISAR RIVAL"):
            model = genai.GenerativeModel("models/gemini-3-flash-preview")
            res = model.generate_content(f"Analise a estratégia da {rival} e aponte brechas.")
            st.markdown(res.text)
    with aba2:
        fb = st.text_area("Feedback do Cliente:")
        if st.button("🧠 PREVER RISCO"):
            model = genai.GenerativeModel("models/gemini-3-flash-preview")
            res = model.generate_content(f"Analise o risco de perda baseado neste texto: {fb}")
            st.markdown(res.text)

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Strategic Edition v2.8")