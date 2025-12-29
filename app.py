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
    .product-header { 
        background: linear-gradient(90deg, #0077b6, #00b4d8); 
        color: white; 
        padding: 20px; 
        border-radius: 10px; 
        margin-bottom: 25px; 
    }
    .stButton > button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3.5em; 
        font-weight: bold; 
        background-color: #0077b6;
        color: white;
    }
    .stTextArea textarea { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIGURAÇÃO DA API ---
# O sistema busca a chave nas variáveis de ambiente por segurança
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# --- 4. BARRA LATERAL (NAVEGAÇÃO DO HUB) ---
with st.sidebar:
    st.title("⚡ TechnoBolt IA")
    st.markdown("---")
    
    st.subheader("Escolha a Ferramenta")
    menu = st.radio(
        "Navegação:",
        ["Página Inicial", "Gerador de Email Inteligente", "Gerador de Briefing Negocial"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    if not api_key:
        st.error("⚠️ API Key não configurada no sistema.")
    st.caption(f"Versão 1.3.0 | Dezembro 2025")
    st.caption("Tecnologia de IA Generativa")

# --- 5. LÓGICA DAS PÁGINAS ---

# --- TELA: PÁGINA INICIAL ---
if menu == "Página Inicial":
    st.markdown('<div class="main-title">TechnoBolt IA ⚡</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Seu Hub Corporativo de Inteligência Artificial.</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🚀 Transformação Digital com IA
    O **TechnoBolt IA** centraliza ferramentas avançadas para otimizar a rotina de gestores e executivos. 
    Toda a nossa tecnologia é baseada em modelos de linguagem de última geração.

    **Explore nossas soluções:**
    
    * **✉️ Gerador de Email Inteligente:** Redija comunicações impecáveis escolhendo o cargo do remetente e o objetivo.
    * **🧠 Gerador de Briefing Negocial:** Receba um raio-x estratégico do mercado com radar de notícias via tags personalizadas.
    
    ---
    *Selecione uma ferramenta no menu ao lado para começar.*
    """)

# --- TELA: GERADOR DE EMAIL INTELIGENTE ---
elif menu == "Gerador de Email Inteligente":
    st.markdown('<div class="product-header">✉️ Gerador de Email Inteligente</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        cargo_ia = st.text_input("Qual cargo a IA deve assumir?", placeholder="Ex: Diretor de Vendas, Analista Jurídico...")
        destinatario = st.text_input("Para quem você está escrevendo?", placeholder="Ex: CEO da Empresa Alpha, Novo Parceiro...")
        objetivo = st.text_area("Qual o objetivo do e-mail?", placeholder="Ex: Agendar reunião de alinhamento, Solicitar urgência no contrato...")
        tom = st.select_slider("Nível de Formalidade:", options=["Muito Casual", "Cordial/Amigável", "Executivo/Sério", "Urgente/Direto"])
    
    with col2:
        st.markdown("### ✨ E-mail Gerado")
        if st.button("🚀 REDIGIR E-MAIL COM IA"):
            if not api_key:
                st.error("Chave API ausente.")
            elif not cargo_ia or not objetivo:
                st.warning("Preencha o cargo e o objetivo.")
            else:
                with st.spinner("IA processando sua comunicação..."):
                    try:
                        # Usando o motor Gemini 3 Flash da sua lista confirmada
                        model = genai.GenerativeModel("models/gemini-3-flash-preview")
                        
                        prompt_email = f"""
                        Atue como um {cargo_ia} profissional.
                        Escreva um e-mail para {destinatario}.
                        Objetivo central: {objetivo}.
                        Tom de voz: {tom}.

                        Regras de Formatação:
                        - Crie um Assunto profissional.
                        - Use parágrafos claros.
                        - Linguagem persuasiva e correta.
                        """
                        
                        response = model.generate_content(prompt_email)
                        st.text_area("Resultado (pronto para copiar):", response.text, height=450)
                        st.success("E-mail gerado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro na geração: {e}")

# --- TELA: GERADOR DE BRIEFING NEGOCIAL ---
elif menu == "Gerador de Briefing Negocial":
    st.markdown('<div class="product-header">🧠 Gerador de Briefing Negocial</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        empresa = st.text_input("Sua Organização:", placeholder="Ex: TechnoBolt Tech")
        setor = st.text_input("Setor de Atuação:", placeholder="Ex: Varejo, Logística, Saúde...")
        
        # SISTEMA DE TAGS DINÂMICAS: O usuário pode selecionar ou digitar novas
        tags_radar = st.multiselect(
            "Prioridades do Radar (Tags):",
            options=["Novas Leis", "Concorrência", "Inovação", "Macroeconomia", "Dólar", "Tributação"],
            default=["Novas Leis", "Concorrência"],
            help="Escolha as sugestões ou digite sua própria palavra-chave e dê Enter."
        )
        st.caption("💡 Digite temas específicos e pressione Enter para criar novas tags.")

    with col2:
        st.markdown("### 📊 Relatório Estratégico & Notícias")
        if st.button("⚡ ESCANEAR MERCADO E GERAR INSIGHTS"):
            if not api_key:
                st.error("Chave API ausente.")
            elif not empresa or not setor:
                st.warning("Por favor, preencha os dados da empresa e setor.")
            else:
                with st.spinner("IA escaneando notícias recentes e analisando mercado..."):
                    try:
                        model = genai.GenerativeModel("models/gemini-3-flash-preview")
                        temas_str = ", ".join(tags_radar)
                        
                        prompt_briefing = f"""
                        Atue como Chief Strategy Officer (CSO). 
                        Data: {time.strftime('%d/%m/%Y')}.
                        Gere um briefing para {empresa} (Setor: {setor}).
                        Foco exclusivo nas Tags de Radar: {temas_str}.

                        ESTRUTURA:
                        1. 🚩 RADAR DE NOTÍCIAS (Resumo de notícias reais e recentes sobre as tags).
                        2. 📉 IMPACTO NO NEGÓCIO (Como esses fatos afetam especificamente a {empresa}).
                        3. 💡 RECOMENDAÇÃO DE GESTÃO (Qual a ação imediata para a diretoria?).
                        
                        Responda de forma sóbria e executiva em Português.
                        """
                        
                        response = model.generate_content(prompt_briefing)
                        st.markdown(response.text)
                        
                        st.download_button(
                            label="📥 Baixar Briefing Executivo",
                            data=response.text,
                            file_name=f"Briefing_{empresa}_{time.strftime('%d%m')}.md",
                            mime="text/markdown"
                        )
                    except Exception as e:
                        st.error(f"Erro na análise: {e}")

# --- 6. RODAPÉ ---
st.markdown("---")
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Todos os processos protegidos por Inteligência Artificial.")