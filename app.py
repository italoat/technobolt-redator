import streamlit as st
import google.generativeai as genai
import os
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="TechnoBolt IA - Hub Corporativo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded" # Tenta manter aberto no desktop
)

# --- 2. CSS PARA DESIGN PREMIUM E MOBILE FIX ---
st.markdown("""
<style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #ffffff; color: #1e1e1e; }
    
    /* Estilização dos títulos */
    .main-title { font-size: 36px; font-weight: 800; color: #0D1B2A; margin-bottom: 10px; }
    .sub-title { font-size: 16px; color: #415A77; margin-bottom: 30px; }
    
    /* Header dos produtos */
    .product-header { 
        background: linear-gradient(90deg, #0077b6, #00b4d8); 
        color: white; padding: 20px; border-radius: 10px; margin-bottom: 25px; 
    }

    /* Botão estilizado */
    .stButton > button { 
        width: 100%; border-radius: 8px; height: 3.5em; 
        font-weight: bold; background-color: #0077b6; color: white; border: none;
    }

    /* ALERTA MOBILE: Instrução visual para achar o menu */
    @media (max-width: 768px) {
        .mobile-instruction {
            background-color: #ff4b4b;
            color: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            margin-bottom: 20px;
            font-weight: bold;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DA API ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 4. ESTADO DE SESSÃO (TAGS) ---
if 'tags_disponiveis' not in st.session_state:
    st.session_state.tags_disponiveis = ["Novas Leis", "Concorrência", "Inovação", "Macroeconomia"]

# --- 5. BARRA LATERAL ---
with st.sidebar:
    st.title("⚡ TechnoBolt IA")
    st.markdown("---")
    menu = st.radio(
        "Menu de Ferramentas:",
        ["Página Inicial", "Gerador de Email Inteligente", "Gerador de Briefing Negocial", "Analista de Atas de Governança"]
    )
    st.markdown("---")
    st.caption(f"v1.6.0 | Dezembro 2025")

# --- 6. LÓGICA DAS PÁGINAS ---

if menu == "Página Inicial":
    # Instrução visual apenas para mobile
    st.markdown('<div class="mobile-instruction">📱 Toque na seta ( > ) no canto superior esquerdo para ver o menu!</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Hub estratégico de produtividade movido por Inteligência Artificial de última geração.</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🚀 Bem-vindo ao seu ecossistema de IA
    Nossas ferramentas automatizam processos complexos para o mundo corporativo privado.
    
    * **✉️ Gerador de Email Inteligente:** Comunicação profissional baseada no seu cargo.
    * **🧠 Gerador de Briefing Negocial:** Radar estratégico com tags personalizadas.
    * **📝 Analista de Atas de Governança:** Formalização ágil de reuniões de diretoria.
    """)

elif menu == "Gerador de Email Inteligente":
    st.markdown('<div class="product-header">✉️ Gerador de Email Inteligente</div>', unsafe_allow_html=True)
    cargo = st.text_input("Seu Cargo:", placeholder="Ex: Diretor de Operações")
    destinatario = st.text_input("Destinatário:", placeholder="Ex: Conselho Administrativo")
    objetivo = st.text_area("Objetivo:", placeholder="Ex: Comunicar resultado trimestral")
    
    if st.button("🚀 GERAR COM IA"):
        with st.spinner("Redigindo..."):
            model = genai.GenerativeModel("models/gemini-3-flash-preview")
            res = model.generate_content(f"Como {cargo}, escreva para {destinatario} sobre {objetivo}.")
            st.text_area("Resultado:", res.text, height=300)

elif menu == "Gerador de Briefing Negocial":
    st.markdown('<div class="product-header">🧠 Gerador de Briefing Negocial</div>', unsafe_allow_html=True)
    empresa = st.text_input("Empresa:", "Sua Empresa")
    setor = st.text_input("Setor:", "Varejo")
    
    tags = st.multiselect("Tags do Radar:", options=st.session_state.tags_disponiveis, default=["Novas Leis"])
    nova_tag = st.text_input("➕ Adicionar nova tag:")
    if nova_tag and nova_tag not in st.session_state.tags_disponiveis:
        st.session_state.tags_disponiveis.append(nova_tag)
        st.rerun()

    if st.button("⚡ ESCANEAR MERCADO"):
        with st.spinner("Analisando notícias..."):
            model = genai.GenerativeModel("models/gemini-3-flash-preview")
            prompt = f"Gere um briefing para {empresa} no setor {setor} focado em: {', '.join(tags)}."
            res = model.generate_content(prompt)
            st.markdown(res.text)

elif menu == "Analista de Atas de Governança":
    st.markdown('<div class="product-header">📝 Analista de Atas de Governança</div>', unsafe_allow_html=True)
    st.info("Transforme notas de reunião em documentos formais de diretoria.")
    
    notas = st.text_area("Notas da Reunião (Tópicos discutidos):", height=200, placeholder="Ex: João aprovou orçamento; Maria sugeriu nova data...")
    tipo = st.selectbox("Tipo de Ata:", ["Reunião de Diretoria", "Conselho de Administração", "Comitê Técnico"])
    
    if st.button("📝 GERAR ATA FORMAL"):
        if not notas:
            st.warning("Insira as notas da reunião.")
        else:
            with st.spinner("IA formalizando o documento..."):
                try:
                    model = genai.GenerativeModel("models/gemini-3-flash-preview")
                    prompt_ata = f"""
                    Atue como Secretário de Governança Corporativa.
                    Transforme as seguintes notas em uma Ata de {tipo} formal e profissional.
                    Notas: {notas}
                    
                    ESTRUTURA:
                    - Título Formal e Data
                    - Participantes (se citados)
                    - Deliberações e Decisões
                    - Tarefas e Responsáveis
                    - Encerramento
                    """
                    response = model.generate_content(prompt_ata)
                    st.markdown("---")
                    st.markdown(response.text)
                    st.download_button("📥 Baixar Ata (.md)", response.text, file_name="ata_reuniao.md")
                except Exception as e:
                    st.error(f"Erro: {e}")

st.markdown("---")
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')}")