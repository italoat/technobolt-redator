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

# --- 2. CSS PARA DESIGN PREMIUM ---
st.markdown("""
<style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #ffffff; color: #1e1e1e; }
    .main-title { font-size: 42px; font-weight: 800; color: #0D1B2A; margin-bottom: 10px; }
    .sub-title { font-size: 18px; color: #415A77; margin-bottom: 30px; }
    .product-header { background: linear-gradient(90deg, #0077b6, #00b4d8); color: white; padding: 20px; border-radius: 10px; margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DA API ---
# Se a chave vazou, gere uma nova e use no terminal ou cole abaixo para teste privado
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 4. BARRA LATERAL (NAVEGAÇÃO DO HUB) ---
with st.sidebar:
    st.title("⚡ TechnoBolt IA")
    st.markdown("---")
    
    st.subheader("🛠️ Ferramentas")
    menu = st.radio(
        "Escolha o que deseja fazer:",
        ["Página Inicial", "Gerador de Email Inteligente", "Gerador de Briefing Negocial"]
    )
    
    st.markdown("---")
    if not api_key:
        st.warning("⚠️ Chave API não detectada.")
    st.caption("v1.1.0 - Inteligência Conectada")

# --- 5. LÓGICA DAS PÁGINAS ---

# --- TELA HOME ---
if menu == "Página Inicial":
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Sua central de produtividade movida por modelos de IA de última geração.</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🚀 Bem-vindo ao Futuro do Trabalho
    Nossas ferramentas utilizam **Inteligência Artificial Generativa** para automatizar tarefas complexas.
    
    * **✉️ Gerador de Email Inteligente:** Redija comunicações impecáveis escolhendo o cargo do remetente e o objetivo.
    * **🧠 Gerador de Briefing Negocial:** Receba um raio-x estratégico do mercado e radar de notícias atualizadas.
    
    ---
    *Selecione uma ferramenta ao lado para começar.*
    """)

# --- TELA: GERADOR DE EMAIL INTELIGENTE ---
elif menu == "Gerador de Email Inteligente":
    st.markdown('<div class="product-header">✉️ Gerador de Email Inteligente</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        cargo_ia = st.text_input("Qual cargo a IA deve assumir?", placeholder="Ex: Diretor Comercial, Analista de RH...")
        destinatario = st.text_input("Para quem você está escrevendo?", placeholder="Ex: CEO da Empresa X, Novo Cliente...")
        objetivo = st.text_area("O que você deseja com esse e-mail? (Objetivo)", placeholder="Ex: Agendar uma demonstração do software, Pedir feedback sobre a proposta...")
        tom = st.select_slider("Nível de Formalidade:", options=["Muito Casual", "Cordial/Amigável", "Executivo/Sério", "Urgente/Direto"])
    
    with col2:
        st.markdown("### ✨ Resultado da IA")
        if st.button("🚀 CRIAR E-MAIL PROFISSIONAL"):
            if not api_key:
                st.error("Configure sua API Key para continuar.")
            elif not cargo_ia or not objetivo:
                st.warning("Preencha o cargo e o objetivo para gerar um bom e-mail.")
            else:
                with st.spinner("A IA está redigindo seu e-mail..."):
                    try:
                        # Usando o motor Gemini 3 que é o topo de linha em 2025
                        model = genai.GenerativeModel("models/gemini-3-flash-preview")
                        
                        prompt_email = f"""
                        Atue como um {cargo_ia} altamente experiente.
                        Escreva um e-mail para {destinatario}.
                        Objetivo do e-mail: {objetivo}.
                        Nível de formalidade e tom: {tom}.

                        Regras:
                        - Crie um Assunto chamativo e profissional.
                        - No corpo, use uma linguagem fluida e persuasiva.
                        - Use parágrafos bem espaçados.
                        """
                        
                        response = model.generate_content(prompt_email)
                        st.write(response.text)
                        st.download_button("📥 Copiar Texto", response.text)
                    except Exception as e:
                        st.error(f"Erro na geração: {e}")

# --- TELA: GERADOR DE BRIEFING NEGOCIAL ---
elif menu == "Gerador de Briefing Negocial":
    st.markdown('<div class="product-header">🧠 Gerador de Briefing Negocial</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        empresa = st.text_input("Nome da sua Empresa:", placeholder="Ex: TechnoBolt Tech")
        setor = st.text_input("Setor de Atuação:", placeholder="Ex: Tecnologia e SaaS")
        foco = st.multiselect("Focar radar em:", ["Leis", "Concorrência", "Tecnologia", "Economia"], default=["Tecnologia"])
    
    with col2:
        st.markdown("### 📊 Relatório & Radar de Notícias")
        if st.button("⚡ ESCANEAR MERCADO"):
            if not api_key:
                st.error("API Key não configurada.")
            elif not empresa or not setor:
                st.warning("Preencha os dados da empresa.")
            else:
                with st.spinner("Analisando notícias e mercado em tempo real..."):
                    try:
                        model = genai.GenerativeModel("models/gemini-3-flash-preview")
                        prompt_briefing = f"""
                        Atue como CSO (Chief Strategy Officer).
                        Gere um briefing para {empresa} no setor de {setor}.
                        Data atual: {time.strftime('%d/%m/%Y')}.

                        ESTRUTURA:
                        1. RADAR DE NOTÍCIAS (Últimas 24-48h impactando {setor} no Brasil).
                        2. ANÁLISE DE IMPACTO EM {', '.join(foco)}.
                        3. RECOMENDAÇÃO DE GESTÃO (O que o CEO deve fazer agora).
                        """
                        response = model.generate_content(prompt_briefing)
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Erro: {e}")

# --- 6. RODAPÉ ---
st.markdown("---")
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Todos os processos protegidos por Inteligência Artificial.")