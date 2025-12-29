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

# --- 2. CSS PARA DESIGN E CORREÇÃO DA VISIBILIDADE MOBILE ---
st.markdown("""
<style>
    /* OCULTA O CABEÇALHO PADRÃO DO STREAMLIT */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* FORÇA A EXIBIÇÃO DO BOTÃO DO MENU (SETA) NO MOBILE */
    /* Criamos um botão flutuante azul no canto superior esquerdo */
    button[kind="headerNoContext"] {
        background-color: #0077b6 !important;
        color: white !important;
        border-radius: 50% !important;
        border: 2px solid #00b4d8 !important;
        visibility: visible !important;
        left: 15px !important;
        top: 15px !important;
        width: 50px !important;
        height: 50px !important;
        z-index: 9999999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
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

    /* ALERTA VISUAL PARA USUÁRIOS DE CELULAR */
    @media (max-width: 768px) {
        .mobile-banner {
            background-color: #f0f2f6;
            border-left: 6px solid #0077b6;
            padding: 15px;
            margin-bottom: 25px;
            font-weight: 600;
            color: #0077b6;
            font-size: 14px;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DA API ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 4. MEMÓRIA DE SESSÃO (TAGS DO RADAR) ---
if 'tags_disponiveis' not in st.session_state:
    st.session_state.tags_disponiveis = ["Novas Leis", "Concorrência", "Tecnologia", "Macroeconomia", "Tributação"]

# --- 5. MENU LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("⚡ TechnoBolt IA")
    st.markdown("---")
    menu = st.radio(
        "Selecione uma solução:",
        ["Página Inicial", "Gerador de Email Inteligente", "Gerador de Briefing Negocial", "Analista de Atas de Governança"]
    )
    st.markdown("---")
    if not api_key:
        st.error("Chave API não configurada.")
    st.caption(f"Versão 1.7.0 | Dezembro 2025")

# --- 6. FLUXO DE TELAS ---

# --- TELA: HOME ---
if menu == "Página Inicial":
    st.markdown('<div class="mobile-banner">⬅️ Toque no círculo azul no canto superior para abrir o menu de ferramentas.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown("##### Suíte estratégica para automação e inteligência corporativa.")
    
    st.markdown("""
    ---
    ### 🛠️ Soluções Disponíveis:
    
    * **✉️ Gerador de Email Inteligente:** Redija comunicações impecáveis baseadas no seu cargo e objetivo.
    * **🧠 Gerador de Briefing Negocial:** Radar estratégico com notícias reais e análise de impacto via tags.
    * **📝 Analista de Atas de Governança:** Formalize reuniões de diretoria em documentos profissionais instantaneamente.
    
    ---
    *Use o menu lateral para alternar entre as ferramentas.*
    """)

# --- TELA: EMAIL ---
elif menu == "Gerador de Email Inteligente":
    st.markdown('<div class="product-header">✉️ Gerador de Email Inteligente</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.2])
    with c1:
        cargo = st.text_input("Cargo da IA:", placeholder="Ex: Diretor Comercial")
        dest = st.text_input("Destinatário:", placeholder="Ex: Conselho Fiscal")
        obj = st.text_area("Objetivo do E-mail:", placeholder="Ex: Justificar desvio de orçamento...")
        tom = st.select_slider("Formalidade:", ["Casual", "Cordial", "Executivo", "Urgente"])
    with c2:
        if st.button("🚀 GERAR E-MAIL PROFISSIONAL"):
            with st.spinner("IA redigindo..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    res = model.generate_content(f"Aja como {cargo}. Escreva para {dest} sobre {obj}. Tom: {tom}.")
                    st.text_area("Conteúdo Gerado:", res.text, height=450)
                except Exception as e: st.error(f"Erro: {e}")

# --- TELA: BRIEFING ---
elif menu == "Gerador de Briefing Negocial":
    st.markdown('<div class="product-header">🧠 Gerador de Briefing Negocial</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.5])
    with c1:
        emp = st.text_input("Nome da Empresa:")
        setor = st.text_input("Setor de Atuação:")
        sel_tags = st.multiselect("Radar de Tags:", options=st.session_state.tags_disponiveis, default=["Novas Leis"])
        nova = st.text_input("➕ Criar nova tag:")
        if nova and nova not in st.session_state.tags_disponiveis:
            st.session_state.tags_disponiveis.append(nova)
            st.rerun()
    with c2:
        if st.button("⚡ ESCANEAR MERCADO"):
            with st.spinner("Buscando notícias e gerando insights..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    prompt = f"Briefing para {emp} ({setor}). Foco: {', '.join(sel_tags)}. Data: {time.strftime('%d/%m/%Y')}."
                    res = model.generate_content(prompt)
                    st.markdown(res.text)
                except Exception as e: st.error(f"Erro: {e}")

# --- TELA: ATAS ---
elif menu == "Analista de Atas de Governança":
    st.markdown('<div class="product-header">📝 Analista de Atas de Governança</div>', unsafe_allow_html=True)
    notas = st.text_area("Notas e deliberações da reunião:", height=250, placeholder="Ex: O Diretor X aprovou o investimento Y...")
    if st.button("📝 FORMALIZAR ATA"):
        with st.spinner("Formatando documento oficial..."):
            try:
                model = genai.GenerativeModel("models/gemini-3-flash-preview")
                res = model.generate_content(f"Transforme em ata de diretoria formal: {notas}")
                st.markdown(res.text)
                st.download_button("📥 Baixar Documento", res.text, file_name="ata.md")
            except Exception as e: st.error(f"Erro: {e}")

# --- RODAPÉ ---
st.markdown("---")
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Powered by Google Gemini 3 Flash")