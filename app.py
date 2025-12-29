import streamlit as st
import google.generativeai as genai
import os
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="TechnoBolt IA - Hub Corporativo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS DEFINITIVO PARA VISIBILIDADE MOBILE ---
st.markdown("""
<style>
    /* OCULTA O CABEÇALHO PADRÃO DO STREAMLIT QUE PODE BLOQUEAR O TOQUE */
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* FORÇA O BOTÃO DO MENU (SETA) A VIRAR UM CÍRCULO AZUL DESTACADO */
    /* Este seletor busca o botão de colapso da barra lateral pelo atributo de teste oficial */
    [data-testid="stSidebarCollapseButton"] {
        background-color: #0077b6 !important;
        color: white !important;
        border-radius: 50% !important;
        width: 55px !important;
        height: 55px !important;
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        z-index: 9999999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.4) !important;
        visibility: visible !important;
    }

    /* Garante que a seta dentro do círculo seja branca e nítida */
    [data-testid="stSidebarCollapseButton"] svg {
        fill: white !important;
        color: white !important;
        width: 32px !important;
        height: 32px !important;
    }

    /* ESTILO GERAL DO HUB */
    .stApp { background-color: #ffffff; color: #1e1e1e; }
    .main-title { font-size: 38px; font-weight: 800; color: #0D1B2A; margin-top: 10px; }
    .product-header { 
        background: linear-gradient(90deg, #0077b6, #00b4d8); 
        color: white; padding: 25px; border-radius: 12px; margin-bottom: 30px; 
    }
    
    /* BOTÕES EXECUTIVOS */
    .stButton > button { 
        width: 100%; border-radius: 10px; height: 3.8em; 
        font-weight: bold; background-color: #0077b6; color: white; border: none;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #00b4d8;
        transform: translateY(-2px);
    }

    /* BANNER DE AJUDA PARA MOBILE */
    @media (max-width: 768px) {
        .mobile-helper {
            background-color: #f0f2f6;
            border-left: 6px solid #0077b6;
            padding: 15px;
            margin-bottom: 25px;
            font-weight: 600;
            color: #0077b6;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DA API ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 4. MEMÓRIA DE SESSÃO (TAGS) ---
if 'tags_disponiveis' not in st.session_state:
    st.session_state.tags_disponiveis = ["Novas Leis", "Concorrência", "Tecnologia", "Macroeconomia", "Tributação"]

# --- 5. MENU LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("⚡ TechnoBolt IA")
    st.markdown("---")
    menu_selecionado = st.radio(
        "Selecione uma ferramenta:",
        ["Página Inicial", "Gerador de Email Inteligente", "Gerador de Briefing Negocial", "Analista de Atas de Governança"]
    )
    st.markdown("---")
    if not api_key:
        st.error("⚠️ Chave API não configurada.")
    st.caption(f"v1.9.0 | Edição Corporativa")

# --- 6. FLUXO DE TELAS ---

# --- TELA: HOME ---
if menu_selecionado == "Página Inicial":
    st.markdown('<div class="mobile-helper">⬅️ Toque no círculo azul acima para abrir o menu de ferramentas.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.write("##### Hub estratégico de produtividade corporativa potencializado por IA.")
    
    st.markdown("""
    ---
    ### 🛠️ Soluções Disponíveis:
    
    * **✉️ Gerador de Email Inteligente:** Redija comunicações impecáveis baseadas no seu cargo e objetivo.
    * **🧠 Gerador de Briefing Negocial:** Radar estratégico com notícias reais e análise de impacto via tags.
    * **📝 Analista de Atas de Governança:** Formalize reuniões de diretoria em documentos profissionais instantaneamente.
    
    ---
    *Utilize o menu lateral para alternar entre as ferramentas.*
    """)

# --- TELA: EMAIL ---
elif menu_selecionado == "Gerador de Email Inteligente":
    st.markdown('<div class="product-header">✉️ Gerador de Email Inteligente</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1.2])
    with col_a:
        cargo = st.text_input("Seu Cargo:", placeholder="Ex: Diretor de Vendas")
        dest = st.text_input("Destinatário:", placeholder="Ex: Conselho de Administração")
        obj = st.text_area("Objetivo do E-mail:", placeholder="Ex: Solicitar aprovação de budget...")
        tom = st.select_slider("Formalidade:", ["Casual", "Cordial", "Executivo", "Urgente"])
    with col_b:
        if st.button("🚀 GERAR COM IA"):
            with st.spinner("Redigindo..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    prompt = f"Como {cargo}, escreva para {dest} sobre {obj}. Tom: {tom}."
                    res = model.generate_content(prompt)
                    st.text_area("Resultado:", res.text, height=450)
                except Exception as e: st.error(f"Erro: {e}")

# --- TELA: BRIEFING ---
elif menu_selecionado == "Gerador de Briefing Negocial":
    st.markdown('<div class="product-header">🧠 Gerador de Briefing Negocial</div>', unsafe_allow_html=True)
    col_c, col_d = st.columns([1, 1.5])
    with col_c:
        emp = st.text_input("Empresa:")
        setor = st.text_input("Setor:")
        sel_tags = st.multiselect("Radar de Tags:", options=st.session_state.tags_disponiveis, default=["Novas Leis"])
        nova = st.text_input("➕ Adicionar nova tag personalizada:")
        if nova and nova not in st.session_state.tags_disponiveis:
            st.session_state.tags_disponiveis.append(nova)
            st.rerun()
    with col_d:
        if st.button("⚡ ESCANEAR MERCADO"):
            with st.spinner("IA processando notícias e mercado..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    p_briefing = f"Briefing para {emp} no setor {setor}. Tags: {', '.join(sel_tags)}. Data: {time.strftime('%d/%m/%Y')}."
                    res = model.generate_content(p_briefing)
                    st.markdown(res.text)
                except Exception as e: st.error(f"Erro: {e}")

# --- TELA: ATAS ---
elif menu_selecionado == "Analista de Atas de Governança":
    st.markdown('<div class="product-header">📝 Analista de Atas de Governança</div>', unsafe_allow_html=True)
    notas = st.text_area("Notas da reunião (tópicos brutos):", height=250)
    if st.button("📝 FORMALIZAR DOCUMENTO"):
        with st.spinner("IA formatando ata oficial..."):
            try:
                model = genai.GenerativeModel("models/gemini-3-flash-preview")
                res = model.generate_content(f"Transforme em ata de diretoria formal: {notas}")
                st.markdown(res.text)
                st.download_button("📥 Baixar Ata (.md)", res.text, file_name="ata.md")
            except Exception as e: st.error(f"Erro: {e}")

# --- RODAPÉ ---
st.markdown("---")
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Estabilidade Mobile v1.9")