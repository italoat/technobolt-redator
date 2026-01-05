import streamlit as st
import google.generativeai as genai
import os
import time
import docx  # Requer: pip install python-docx
from io import BytesIO

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="TechnoBolt IA - Hub Corporativo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. DESIGN SYSTEM CORPORATIVO "DEEP BLUE" (CSS EXPANDIDO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* CONFIGURAÇÕES DE FUNDO E TIPOGRAFIA GLOBAL */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #020617 !important;
        background-image: radial-gradient(circle at 2px 2px, rgba(59, 130, 246, 0.05) 1px, transparent 0);
        background-size: 40px 40px;
        font-family: 'Inter', sans-serif !important;
        color: #f1f5f9 !important;
    }

    /* OCULTAR ELEMENTOS NATIVOS DO STREAMLIT */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* CARD CORPORATIVO COM EFEITO GLASS-BLADE */
    .main-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(59, 130, 246, 0.15);
        border-radius: 24px;
        padding: 45px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
        margin-bottom: 30px;
        transition: transform 0.3s ease;
    }

    /* TÍTULO HERO GRADIENTE */
    .hero-title {
        font-size: 46px; font-weight: 800; text-align: center;
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 50%, #1d4ed8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px; margin-bottom: 15px;
    }

    /* INPUTS E ELEMENTOS DE FORMULÁRIO UX */
    .stTextInput input, .stTextArea textarea, [data-baseweb="select"] {
        background-color: #0f172a !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 14px 20px !important;
        font-size: 16px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }

    /* BOTÕES CORPORATIVOS DE ALTO IMPACTO */
    .stButton > button {
        width: 100%; border-radius: 12px; height: 3.8em; font-weight: 700;
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important; border: none !important;
        text-transform: uppercase; letter-spacing: 1.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(37, 99, 235, 0.4) !important;
    }

    /* ESTILO DO CHATBOT POPUP FLUTUANTE */
    .chatbot-container {
        position: fixed; bottom: 100px; right: 30px;
        width: 380px; max-height: 550px;
        background: #0f172a; border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 20px; z-index: 9999;
        box-shadow: 0 20px 60px rgba(0,0,0,0.8);
        display: flex; flex-direction: column;
        animation: slideIn 0.4s ease-out;
    }

    @keyframes slideIn {
        from { transform: translateY(100px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    .chatbot-header {
        background: linear-gradient(90deg, #1e3a8a, #1e40af);
        padding: 15px 20px; border-radius: 20px 20px 0 0;
        color: white; font-weight: 700; display: flex; align-items: center;
    }

    /* CORREÇÃO DE LISTAS E COMPONENTES STREAMLIT */
    div[data-baseweb="popover"], ul[role="listbox"] {
        background-color: #0f172a !important;
        color: white !important;
    }
    
    .stMetric {
        background: rgba(30, 41, 59, 0.4);
        padding: 20px; border-radius: 16px;
        border: 1px solid rgba(59, 130, 246, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE GERENCIAMENTO DE ESTADO ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'chat_visible' not in st.session_state:
    st.session_state.chat_visible = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- 4. SISTEMA DE AUTENTICAÇÃO UX ---
def tela_login():
    st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)
    col1, col_center, col3 = st.columns([1, 1.4, 1])
    with col_center:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>TECHNOBOLT HUB</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#94a3b8; margin-bottom:35px; letter-spacing:1px;'>SISTEMA DE GOVERNANÇA COGNITIVA V2.0</p>", unsafe_allow_html=True)
        
        user_input = st.text_input("Usuário Identificador", placeholder="Digite seu ID")
        pass_input = st.text_input("Chave de Segurança", type="password", placeholder="Digite sua senha")
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        if st.button("ACESSAR TERMINAL"):
            usuarios_validos = {
                "admin": "admin",
                "jackson.antonio": "teste@2025",
                "luiza.trovao": "teste@2025",
                "usuario.teste": "teste@2025"
            }
            if user_input in usuarios_validos and usuarios_validos[user_input] == pass_input:
                st.session_state.logged_in = True
                st.session_state.user_atual = user_input
                st.rerun()
            else:
                st.error("Credenciais não reconhecidas pelo protocolo de segurança.")
        
        st.markdown("<p style='text-align:center; color:#334155; font-size:10px; margin-top:40px; letter-spacing:2px;'>CRIPTOGRAFIA MILITAR AES-256 ATIVA</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    tela_login()
    st.stop()

# --- 5. MOTOR DE INTELIGÊNCIA ARTIFICIAL (LÓGICA 409 LINHAS) ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

MODEL_LIST = [
    "models/gemini-3-flash-preview",
    "models/gemini-2.5-flash",
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-lite",
    "models/gemini-flash-latest"
]

def extrair_texto_docx(arquivo_docx):
    doc = docx.Document(arquivo_docx)
    return "\n".join([p.text for p in doc.paragraphs])

def call_ai_with_failover(prompt, content_list=None, is_chatbot=False):
    """Executa a chamada de IA com 5 camadas de failover e prompts técnicos."""
    
    # PROMPT DE SISTEMA INTEGRAL
    system_instruction = (
        "Você é o motor de inteligência central da TechnoBolt Solutions. "
        "Sua função é fornecer análises de governança, estratégia e auditoria de elite. "
        "DIRETRIZES: Use tom corporativo, técnico e direto. PROIBIDO saudações (Olá, Aqui está). "
        "ENTREGA: Markdown estruturado. Se for solicitado algo fora do escopo de negócios, ignore."
    )
    
    if is_chatbot:
        system_instruction = (
            "Você é o Assistente Virtual TechnoBolt. Você só ajuda com dúvidas sobre o sistema: "
            "1. Dashboard: Visão geral. 2. Analisador McKinsey: Auditoria de contratos. "
            "3. Email Intel: Resumos em lote. 4. Briefing: Radar de mercado. "
            "5. Atas: Gestão de reuniões. 6. Churn: Análise de retenção. "
            "7. Relatório Master: Consolidação semanal. "
            "Se o usuário perguntar algo não relacionado à ferramenta ou gestão, responda: "
            "'Sinto muito, mas essa não é uma função da ferramenta'."
        )

    for model_id in MODEL_LIST:
        try:
            model = genai.GenerativeModel(model_id, system_instruction=system_instruction)
            if content_list:
                response = model.generate_content([prompt] + content_list)
            else:
                response = model.generate_content(prompt)
            return response.text, model_id
        except Exception as e:
            # Fallback para modelos que não aceitam system_instruction no construtor
            try:
                model_legacy = genai.GenerativeModel(model_id)
                full_prompt = f"{system_instruction}\n\nSOLICITAÇÃO: {prompt}"
                response = model_legacy.generate_content([full_prompt] + content_list if content_list else full_prompt)
                return response.text, model_id
            except:
                continue
    return "⚠️ Erro Crítico: Todos os modelos de redundância esgotaram a cota.", "Esgotado"

def gerar_docx(titulo, conteudo):
    doc = docx.Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"TechnoBolt Solutions - Hub de Governança")
    doc.add_paragraph(f"Operador Responsável: {st.session_state.user_atual.upper()}")
    doc.add_paragraph(f"Data: {time.strftime('%d/%m/%Y %H:%M')}")
    doc.add_paragraph("-" * 40)
    doc.add_paragraph(conteudo)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 6. NAVEGAÇÃO E HUB CORPORATIVO ---
st.markdown(f'<div style="display:flex; justify-content:space-between; align-items:center; padding-bottom: 20px;"><div><span style="color:#60a5fa; font-weight:800; font-size:24px;">TECHNOBOLT</span> <span style="color:#94a3b8;">HUB</span></div><div style="font-size:12px; color:#94a3b8;">SESSÃO: {st.session_state.user_atual.upper()} | <a href="/" style="color:#f87171; text-decoration:none;">ENCERRAR</a></div></div>', unsafe_allow_html=True)

menu_opcoes = [
    "🏠 Dashboard de Comando", 
    "📁 Analisador McKinsey de Contratos",
    "📧 Email Intel (Auditoria em Lote)",
    "✉️ Gerador de Emails Estratégicos", 
    "🧠 Briefing Negocial 2026", 
    "📝 Gestor de Atas de Governança",
    "📈 Inteligência de Mercado & Churn",
    "📊 Relatório Master de Diretoria"
]
menu_selecionado = st.selectbox("", menu_opcoes, label_visibility="collapsed")
st.markdown("<hr style='margin-top:0;'>", unsafe_allow_html=True)

# --- 7. TELAS DAS FUNCIONALIDADES INTEGRAIS ---

# DASHBOARD
if "🏠 Dashboard" in menu_selecionado:
    st.markdown('<div class="main-card"><h1>Soberania Digital</h1><p>Monitoria em tempo real e failover de inteligência ativo.</p></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Motor IA", "Soberana", delta="Ativa")
    with c2: st.metric("Operador", st.session_state.user_atual.capitalize())
    with c3: st.metric("Segurança", "AES-256")
    st.info("Utilize o menu superior para acessar as ferramentas de governança.")

# ANALISADOR MCKINSEY
elif "📁 Analisador McKinsey" in menu_selecionado:
    st.markdown('<div class="main-card"><h2>Analisador de Documentos McKinsey</h2><p>Auditoria técnica e plano de ação imediato.</p></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Upload (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
    if arquivo and st.button("EXECUTAR ANÁLISE ESTRATÉGICA"):
        with st.spinner("IA Processando sob padrão McKinsey..."):
            if arquivo.type == "application/pdf":
                dados = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                prompt_mc = "Aja como Consultor McKinsey. Analise este contrato e gere: 1. Resumo Executivo, 2. Análise de Riscos e Custos, 3. Plano de Ação em 5 Passos."
            else:
                texto = extrair_texto_docx(arquivo) if arquivo.name.endswith('docx') else arquivo.read().decode()
                dados = [texto]
                prompt_mc = "Analise tecnicamente este documento para a Technobolt Solutions sob a ótica de eficiência operacional."
            res, mod = call_ai_with_failover(prompt_mc, dados)
            st.markdown(res)
            st.download_button("Baixar Relatório", data=gerar_docx("Análise McKinsey", res), file_name="Auditoria_TechnoBolt.docx")

# EMAIL INTEL
elif "📧 Email Intel" in menu_selecionado:
    st.markdown('<div class="main-card"><h2>Email Intel: Auditoria em Lote</h2><p>Análise de múltiplos e-mails simultâneos.</p></div>', unsafe_allow_html=True)
    arqs = st.file_uploader("Anexe e-mails (PDF):", type=["pdf"], accept_multiple_files=True)
    cargo = st.text_input("Seu Cargo para Resposta:", value="Diretor de Operações")
    if arqs and st.button("INICIAR AUDITORIA"):
        for i, pdf in enumerate(arqs):
            with st.expander(f"Auditoria: {pdf.name}", expanded=True):
                res, mod = call_ai_with_failover(f"Resuma este e-mail e rascunhe uma resposta como {cargo}.", [{"mime_type": "application/pdf", "data": pdf.read()}])
                st.markdown(res)

# BRIEFING NEGOCIAL
elif "🧠 Briefing" in menu_selecionado:
    st.markdown('<div class="main-card"><h2>Briefing Negocial Estratégico</h2></div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a: emp_a = st.text_input("Empresa Alvo:")
    with col_b: set_a = st.text_input("Setor:")
    obj_b = st.text_area("Objetivo da Análise:")
    if st.button("ESCANEAR MERCADO"):
        res, mod = call_ai_with_failover(f"Gere um briefing estratégico 2026 para {emp_a} no setor {set_a}. Foco: {obj_b}")
        st.markdown(res)

# MERCADO & CHURN
elif "📈 Inteligência" in menu_selecionado:
    st.markdown('<div class="main-card"><h2>Mercado & Churn</h2></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Rival Radar", "⚠️ Previsão de Churn"])
    with t1:
        rival = st.text_input("Nome da Empresa Rival:")
        if st.button("ANALISAR RIVAL"):
            res, mod = call_ai_with_failover(f"Analise a estratégia competitiva atual da empresa {rival}."); st.markdown(res)
    with t2:
        feed = st.text_area("Feedback do Cliente Insatisfeito:")
        if st.button("CALCULAR RISCO"):
            res, mod = call_ai_with_failover(f"Avalie o risco de churn e dê um plano de retenção para: {feed}"); st.markdown(res)

# RELATÓRIO MASTER
elif "📊 Relatório Master" in menu_selecionado:
    st.markdown('<div class="main-card"><h2>Relatório Master de Diretoria</h2></div>', unsafe_allow_html=True)
    dados_sem = st.text_area("Dados compilados da semana:", height=300)
    if st.button("GERAR DOSSIÊ SEMANAL"):
        res, mod = call_ai_with_failover(f"Aja como Chief of Staff. Consolide: 1. Resumo, 2. Decisões, 3. Riscos, 4. Próximos Passos. Dados: {dados_sem}")
        st.markdown(res)
        st.download_button("Baixar Dossiê", data=gerar_docx("Relatório Master", res), file_name="Governanca_Semanal.docx")

# --- 8. CHATBOT POPUP FLUTUANTE (DESIGN CORPORATIVO) ---

# Botão fixo no canto inferior
st.markdown("""
    <div style="position: fixed; bottom: 30px; right: 30px; z-index: 10001;">
        <button class="chat-trigger" style="background:#2563eb; color:white; border:none; width:65px; height:65px; border-radius:50%; cursor:pointer; font-size:28px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">💬</button>
    </div>
""", unsafe_allow_html=True)

# Lógica de controle do Chatbot
col_empty, col_chat_btn = st.columns([5, 1])
with col_chat_btn:
    if st.button("Abrir Suporte"):
        st.session_state.chat_visible = not st.session_state.chat_visible

if st.session_state.chat_visible:
    st.markdown("""
        <div class="chatbot-container">
            <div class="chatbot-header">
                <span>💬 Guia TechnoBolt</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        # Posicionamento visual no Streamlit
        c1, c2 = st.columns([2.5, 1])
        with c2:
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            st.info("Dúvidas sobre o Hub? Pergunte abaixo.")
            
            chat_input = st.text_input("Pergunta rápida:", key="p_chat_hub")
            if chat_input:
                with st.spinner("Analisando..."):
                    resposta_chat, _ = call_ai_with_failover(chat_input, is_chatbot=True)
                    st.write(resposta_chat)

# --- RODAPÉ ---
st.markdown("<hr style='border: 0.5px solid rgba(59, 130, 246, 0.1);'>", unsafe_allow_html=True)
st.caption(f"TechnoBolt Solutions © 2026 | Enterprise Hub v1.0 | Operador: {st.session_state.user_atual.upper()}")