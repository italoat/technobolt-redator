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

# --- 2. CSS PARA DARK MODE TOTAL, FONTES BRANCAS E UI EXECUTIVA ---
st.markdown("""
<style>
    /* OCULTA ELEMENTOS PADRÃO DO STREAMLIT QUE POLUEM O DESIGN */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* FUNDO ESCURO PROFUNDO (ESTILO GITHUB DARK / VESTA) */
    .stApp { 
        background-color: #0d1117 !important; 
        color: #ffffff !important; 
    }

    /* FORÇA TODAS AS FONTES, LABELS E TEXTOS PARA BRANCO PURO */
    h1, h2, h3, h4, h5, h6, p, label, span, div, .stMarkdown, [data-testid="stWidgetLabel"] p { 
        color: #ffffff !important; 
    }

    /* TÍTULO PRINCIPAL CENTRALIZADO */
    .main-title { 
        font-size: 36px; 
        font-weight: 800; 
        color: #ffffff !important; 
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }

    /* CABEÇALHO DAS FERRAMENTAS (GRADIENTE DARK SUTIL) */
    .product-header { 
        background: linear-gradient(90deg, #161b22, #0d1117); 
        color: #ffffff !important; 
        padding: 22px; 
        border-radius: 12px; 
        margin-bottom: 30px;
        text-align: center;
        border: 1px solid #30363d;
    }

    /* ESTILIZAÇÃO DO MENU SUPERIOR (SELECTBOX) PARA DARK MODE */
    div[data-baseweb="select"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    
    div[data-baseweb="select"] * {
        color: #ffffff !important;
        background-color: transparent !important;
    }

    /* ESTILO PARA INPUTS E TEXTAREAS */
    .stTextInput input, .stTextArea textarea {
        background-color: #0d1117 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }

    /* ESTILO PARA O SLIDER DE FORMALIDADE */
    .stSlider [data-testid="stTickBarMin"], .stSlider [data-testid="stTickBarMax"], .stSlider span {
        color: #ffffff !important;
    }

    /* BOTÃO GERAR (VERDE CORPORATIVO) */
    .stButton > button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3.8em; 
        font-weight: bold; 
        background-color: #238636 !important; 
        color: #ffffff !important; 
        border: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #2ea043 !important;
        transform: translateY(-2px);
    }
    
    /* TAGS DO MULTISELECT */
    span[data-baseweb="tag"] {
        background-color: #388bfd !important;
        color: #ffffff !important;
    }

    /* LINHA DIVISORA */
    hr { border: 0.5px solid #30363d !important; }

</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DA API ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 4. SISTEMA DE NAVEGAÇÃO SUPERIOR (DENTRO DA PÁGINA) ---
st.markdown('<div style="text-align: center; font-weight: bold; color: #58a6ff; margin-top: 15px; font-size: 13px; letter-spacing: 1px;">CENTRAL DE COMANDO</div>', unsafe_allow_html=True)
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
    st.session_state.tags_disponiveis = ["Novas Leis", "Concorrência", "Tecnologia", "Macroeconomia", "Mercado Financeiro"]

# --- 6. TELAS DO HUB ---

# --- TELA: HOME ---
if "🏠 Página Inicial" in menu_selecionado:
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #8b949e !important;'>Hub estratégico de produtividade corporativa em ambiente Dark Mode.</p>", unsafe_allow_html=True)
    
    st.markdown("""
    ### 🚀 Soluções de Elite
    Selecione a ferramenta no menu superior para começar:
    
    * **✉️ Gerador de Email:** Redação executiva com ajuste fino de cargo e formalidade.
    * **🧠 Briefing Negocial:** Radar estratégico em tempo real baseado em suas palavras-chave.
    * **📝 Analista de Atas:** Transformação de decisões verbais em documentos formais de governança.
    
    ---
    *Otimizado para desktops e dispositivos móveis (iOS/Android).*
    """)

# --- TELA: GERADOR DE EMAIL ---
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header">✉️ Gerador de Email Inteligente</div>', unsafe_allow_html=True)
    
    cargo = st.text_input("Qual cargo a IA deve assumir?", placeholder="Ex: Diretor de Operações")
    dest = st.text_input("Para quem você está escrevendo?", placeholder="Ex: CEO da Empresa X")
    obj = st.text_area("Objetivo da comunicação:", placeholder="Ex: Solicitar urgência no faturamento da nota...")
    
    # REINTEGRAÇÃO DA BARRA DE FORMALIDADE
    formalidade = st.select_slider(
        "Nível de Formalidade do Texto:",
        options=["Muito Casual", "Cordial/Amigável", "Executivo/Padrão", "Formal/Rígido", "Urgente/Direto"],
        value="Executivo/Padrão"
    )
    
    if st.button("🚀 GERAR COMUNICAÇÃO EXECUTIVA"):
        if not cargo or not obj:
            st.warning("Por favor, preencha o cargo e o objetivo para continuar.")
        else:
            with st.spinner("IA redigindo conteúdo profissional..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    prompt = f"""
                    Atue como um {cargo} altamente profissional. 
                    Escreva um e-mail para {dest}. 
                    Objetivo: {obj}. 
                    Tom: {formalidade}.
                    Importante: Use fontes brancas na resposta final.
                    """
                    response = model.generate_content(prompt)
                    st.text_area("Cópia disponível:", response.text, height=450)
                except Exception as e:
                    st.error(f"Erro na geração: {e}")

# --- TELA: BRIEFING NEGOCIAL ---
elif "🧠 Gerador de Briefing" in menu_selecionado:
    st.markdown('<div class="product-header">🧠 Gerador de Briefing Negocial</div>', unsafe_allow_html=True)
    
    empresa = st.text_input("Nome da sua Empresa:")
    setor = st.text_input("Setor de Atuação:")
    tags_radar = st.multiselect("Prioridades do Radar:", options=st.session_state.tags_disponiveis, default=["Novas Leis"])
    
    nova_t = st.text_input("➕ Adicionar Tag Personalizada:")
    if nova_t and nova_t not in st.session_state.tags_disponiveis:
        st.session_state.tags_disponiveis.append(nova_t)
        st.rerun()

    if st.button("⚡ ESCANEAR MERCADO E TAGS"):
        if not empresa or not setor:
            st.warning("Informe os dados da empresa para o radar.")
        else:
            with st.spinner("Analisando notícias e impactos de 2025..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    p_briefing = f"Gere briefing executivo para {empresa} ({setor}). Foco: {', '.join(tags_radar)}."
                    response = model.generate_content(p_briefing)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Erro: {e}")

# --- TELA: ANALISTA DE ATAS ---
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header">📝 Analista de Atas de Governança</div>', unsafe_allow_html=True)
    
    notas = st.text_area("Decisões e tópicos da reunião:", height=250, placeholder="Ex: Diretor Financeiro aprovou budget extra para marketing...")
    
    if st.button("📝 GERAR DOCUMENTO FORMAL"):
        if not notas:
            st.warning("Insira as notas da reunião para formalizar.")
        else:
            with st.spinner("IA estruturando ata oficial..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    response = model.generate_content(f"Transforme em uma ata de diretoria formal e estruturada: {notas}")
                    st.markdown(response.text)
                    st.download_button("📥 Baixar em Markdown", response.text, file_name="ata_governanca.md")
                except Exception as e:
                    st.error(f"Erro: {e}")

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Full Dark v2.5 stable")