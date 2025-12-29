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

# --- 2. CSS PARA DARK MODE TOTAL E FONTES BRANCAS ---
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

    /* FORÇA TODAS AS FONTES E RÓTULOS PARA BRANCO */
    h1, h2, h3, h4, h5, h6, p, label, span, div, .stMarkdown { 
        color: #ffffff !important; 
    }

    /* TÍTULOS E SUBTÍTULOS */
    .main-title { 
        font-size: 34px; 
        font-weight: 800; 
        color: #ffffff !important; 
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 14px;
        color: #8b949e !important;
        text-align: center;
        margin-bottom: 25px;
    }

    /* CABEÇALHO DAS FERRAMENTAS (GRADIENTE DARK) */
    .product-header { 
        background: linear-gradient(90deg, #161b22, #0d1117); 
        color: #ffffff !important; 
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid #30363d;
    }

    /* ESTILO DOS INPUTS, TEXTAREAS E SELECTBOXES (DARK) */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }

    /* BOTÕES EXECUTIVOS (AZUL COBALTO) */
    .stButton > button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3.5em; 
        font-weight: bold; 
        background-color: #238636 !important; /* Verde Sucesso Corporativo */
        color: #ffffff !important; 
        border: none;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #2ea043 !important;
        transform: translateY(-1px);
    }

    /* AJUSTE PARA O MULTISELECT (TAGS) */
    span[data-baseweb="tag"] {
        background-color: #30363d !important;
        color: #ffffff !important;
        border-radius: 4px !important;
    }

    /* LINHA DIVISORA DARK */
    hr { border: 0.5px solid #30363d !important; }

</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DA API ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 4. SISTEMA DE NAVEGAÇÃO SUPERIOR (IDEAL PARA MOBILE) ---
st.markdown('<div style="text-align: center; font-weight: bold; color: #58a6ff; margin-top: 10px; font-size: 12px;">HUB DE FERRAMENTAS</div>', unsafe_allow_html=True)
menu_opcoes = [
    "🏠 Página Inicial", 
    "✉️ Gerador de Email Inteligente", 
    "🧠 Gerador de Briefing Negocial", 
    "📝 Analista de Atas de Governança"
]
menu_selecionado = st.selectbox("Menu", menu_opcoes, label_visibility="collapsed")

st.markdown("<hr>", unsafe_allow_html=True)

# --- 5. MEMÓRIA DE SESSÃO (TAGS) ---
if 'tags_disponiveis' not in st.session_state:
    st.session_state.tags_disponiveis = ["Novas Leis", "Concorrência", "Inovação", "Macroeconomia", "Carga Tributária"]

# --- 6. TELAS DO HUB ---

# --- HOME ---
if "🏠 Página Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Inteligência Artificial para a Alta Gestão Privada.</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🚀 Soluções Corporativas
    Use o seletor no topo para navegar entre os módulos:
    
    * **✉️ Gerador de Email:** Redação executiva precisa com ajuste de cargo e tom.
    * **🧠 Briefing Negocial:** Monitoramento de mercado e radar estratégico via tags.
    * **📝 Analista de Atas:** Transformação de notas brutas em documentos formais.
    
    ---
    *Interface otimizada para visualização em dispositivos móveis e desktops.*
    """)

# --- GERADOR DE EMAIL ---
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header">✉️ Gerador de Email Inteligente</div>', unsafe_allow_html=True)
    
    cargo = st.text_input("Qual cargo a IA deve assumir?", placeholder="Ex: Diretor Sênior de RH")
    dest = st.text_input("Para quem você escreve?", placeholder="Ex: CEO da Empresa Parceira")
    obj = st.text_area("Objetivo da comunicação:", placeholder="Ex: Solicitar renegociação de prazos...")
    
    if st.button("🚀 GERAR COMUNICAÇÃO"):
        if not api_key: st.error("Erro: API Key não configurada.")
        elif not cargo or not obj: st.warning("Preencha o cargo e o objetivo.")
        else:
            with st.spinner("Redigindo e-mail executivo..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    prompt = f"Como {cargo}, escreva para {dest} sobre {obj}. Use fontes claras e tom executivo sênior."
                    response = model.generate_content(prompt)
                    st.text_area("Cópia Final:", response.text, height=400)
                except Exception as e: st.error(f"Erro na IA: {e}")

# --- BRIEFING NEGOCIAL ---
elif "🧠 Gerador de Briefing" in menu_selecionado:
    st.markdown('<div class="product-header">🧠 Gerador de Briefing Negocial</div>', unsafe_allow_html=True)
    
    empresa = st.text_input("Nome da sua Empresa:")
    setor = st.text_input("Setor de Atuação:")
    tags_sel = st.multiselect("Radar de Prioridades:", options=st.session_state.tags_disponiveis, default=["Novas Leis"])
    
    nova = st.text_input("➕ Adicionar Tag Livre:")
    if nova and nova not in st.session_state.tags_disponiveis:
        st.session_state.tags_disponiveis.append(nova)
        st.rerun()

    if st.button("⚡ ESCANEAR MERCADO"):
        if not empresa or not setor: st.warning("Informe os dados básicos da empresa.")
        else:
            with st.spinner("IA processando radar de notícias 2025..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    prompt_b = f"Gere briefing executivo para {empresa} ({setor}). Foco: {', '.join(tags_sel)}."
                    response = model.generate_content(prompt_b)
                    st.markdown(response.text)
                except Exception as e: st.error(f"Erro: {e}")

# --- ANALISTA DE ATAS ---
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header">📝 Analista de Atas de Governança</div>', unsafe_allow_html=True)
    
    notas = st.text_area("Notas e decisões da reunião (tópicos):", height=250, placeholder="Ex: João aprovou projeto; Orçamento reduzido em 10%...")
    
    if st.button("📝 FORMALIZAR ATA"):
        if not notas: st.warning("Insira as notas da reunião.")
        else:
            with st.spinner("IA estruturando documento oficial..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    response = model.generate_content(f"Transforme em ata de diretoria formal e estruturada: {notas}")
                    st.markdown(response.text)
                    st.download_button("📥 Baixar Documento (.md)", response.text, file_name="ata_governanca.md")
                except Exception as e: st.error(f"Erro: {e}")

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Corporativo Dark v2.3")