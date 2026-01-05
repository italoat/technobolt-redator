import streamlit as st
import google.generativeai as genai
import os
import time
import docx  # Requer: pip install python-docx
from io import BytesIO

# --- 1. CONFIGURAÇÃO DE SEGURANÇA E PROTOCOLO ---
st.set_page_config(
    page_title="TechnoBolt IA - Elite Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. GESTÃO DE ESTADO (PERSISTÊNCIA DE SESSÃO) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_atual' not in st.session_state:
    st.session_state.user_atual = None
if 'chat_active' not in st.session_state:
    st.session_state.chat_active = False

def protocol_logout():
    """Finaliza a sessão e limpa os estados de segurança."""
    st.session_state.logged_in = False
    st.session_state.user_atual = None
    st.rerun()

# --- 3. DESIGN SYSTEM (LIGHT CORPORATE EXCLUSIVE - ZERO BUG) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* BASE LIGHT MODE CORPORATIVO */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
        color: #0f172a !important;
    }

    [data-testid="stSidebar"] { display: none !important; }
    header, footer { visibility: hidden !important; }

    /* CARTÃO CORPORATIVO ELITE */
    .main-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 45px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04);
        margin-bottom: 30px;
    }

    .hero-title {
        font-size: 42px; font-weight: 800; text-align: center;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
    }

    /* INPUTS UX CORPORATIVO */
    .stTextInput input, .stTextArea textarea, [data-baseweb="select"], .stSelectbox div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        color: #0f172a !important;
        padding: 14px 18px !important;
        transition: 0.3s all ease;
    }
    
    .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }

    /* BOTÃO TECHNOBOLT EXCLUSIVE */
    .stButton > button {
        width: 100%; border-radius: 14px; height: 3.8em; font-weight: 700;
        background: #1e40af !important; color: white !important; border: none !important;
        text-transform: uppercase; letter-spacing: 1.5px; transition: 0.3s;
        display: flex; align-items: center; justify-content: center;
    }
    .stButton > button:hover {
        background: #1e3a8a !important; transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(30, 64, 175, 0.25) !important;
    }
    .stButton > button div[data-testid="stMarkdownContainer"] p {
        background: none !important; color: white !important; margin: 0 !important;
        padding: 0 !important; text-shadow: none !important;
    }

    /* CHATBOT POPUP LATERAL (ESTÁVEL) */
    .chat-popup {
        position: fixed; bottom: 100px; right: 30px; width: 380px;
        background: white; border: 1px solid #1e40af; border-radius: 25px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.15); z-index: 9999; overflow: hidden;
    }
    .chat-header { background: #1e40af; color: white; padding: 20px; font-weight: 700; text-align: center; }

    /* NAVEGAÇÃO SUPERIOR */
    .top-nav {
        display: flex; justify-content: space-between; align-items: center;
        padding: 20px 40px; background: white; border-bottom: 1px solid #e2e8f0;
        margin-bottom: 40px; border-radius: 0 0 20px 20px;
    }
    
    .status-badge {
        padding: 6px 16px; border-radius: 50px; background: #eff6ff; 
        color: #1e40af; font-size: 11px; font-weight: 700; border: 1px solid #dbeafe;
    }

    .metric-container {
        background: #ffffff; padding: 25px; border-radius: 20px;
        border: 1px solid #e2e8f0; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. TELA DE LOGIN (DESIGN CLEAN CENTRALIZADO) ---
def show_login_screen():
    st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1.4, 1])
    with col_login:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>TECHNOBOLT HUB</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#64748b; margin-bottom:40px; letter-spacing:1px;'>GOVERNANÇA COGNITIVA & IA ELITE</p>", unsafe_allow_html=True)
        
        user_input = st.text_input("Credencial Identificadora", placeholder="Usuário")
        pass_input = st.text_input("Chave de Segurança", type="password", placeholder="Senha")
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        if st.button("AUTENTICAR NO TERMINAL"):
            credenciais = {"admin": "admin", "jackson.antonio": "teste@2025", "luiza.trovao": "teste@2025"}
            if user_input in credenciais and credenciais[user_input] == pass_input:
                st.session_state.logged_in = True
                st.session_state.user_atual = user_input
                st.rerun()
            else:
                st.error("Protocolo negado. Credenciais inválidas.")
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    show_login_screen()
    st.stop()

# --- 5. MOTOR DE IA COM FAILOVER DE 5 NÍVEIS (ALTA DISPONIBILIDADE) ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# CADEIA DE REDUNDÂNCIA (FAILOVER)
AI_MODELS_PRIORITY = [
    "models/gemini-1.5-pro",
    "models/gemini-1.5-flash-latest",
    "models/gemini-1.5-flash",
    "models/gemini-1.0-pro",
    "models/gemini-pro"
]

def call_technobolt_ai(prompt, media=None, mode_explainer=False):
    """Executa a requisição com redundância automática e prompts McKinsey."""
    system_instruction = (
        "Você é o Motor de Inteligência Estratégica da TechnoBolt Solutions. "
        "Sua postura é de um consultor sênior McKinsey/BCG/Bain. "
        "DIRETRIZES: 1. Respostas técnicas, analíticas e extremamente detalhadas. 2. Use terminologia executiva. "
        "3. Markdown estruturado com tabelas e gráficos textuais. 4. Foco total em ROI, Governança e Riscos. "
        "Proibido saudações genéricas ou conversas informais. Vá direto ao ponto técnico."
    )
    
    if mode_explainer:
        system_instruction = (
            "Você é o Guia de Integração TechnoBolt. Explique de forma didática e executiva como "
            "cada módulo do Hub resolve dores de negócio e gera eficiência operacional."
        )

    for model_name in AI_MODELS_PRIORITY:
        try:
            model = genai.GenerativeModel(model_name, system_instruction=system_instruction)
            payload = [prompt] + media if media else prompt
            response = model.generate_content(payload)
            return response.text, model_name
        except Exception:
            continue
    return "⚠️ CRITICAL_ERROR: Todos os motores de redundância falharam.", "OFFLINE"

def export_to_docx(title, content):
    """Gera um arquivo Microsoft Word com formatação corporativa."""
    doc = docx.Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(f"Relatório de Governança | Operador: {st.session_state.user_atual.upper()}")
    doc.add_paragraph(f"Timestamp: {time.strftime('%d/%m/%Y %H:%M')}")
    doc.add_paragraph("-" * 50)
    doc.add_paragraph(content)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 6. CABEÇALHO E NAVEGAÇÃO SUPERIOR ---
st.markdown(f"""
<div class="top-nav">
    <div style="font-weight: 800; color: #1e40af; font-size: 24px;">TECHNOBOLT <span style="color:#64748b; font-weight:400;">ELITE HUB</span></div>
    <div style="display:flex; align-items:center; gap: 25px;">
        <span class="status-badge">SESSÃO: {st.session_state.user_atual.upper()}</span>
    </div>
</div>
""", unsafe_allow_html=True)

col_sp, col_exit = st.columns([10, 1.2])
with col_exit:
    if st.button("🚪 SAIR", key="btn_logout"):
        protocol_logout()

menu_list = [
    "🏠 Dashboard de Comando",
    "📁 Analisador McKinsey",
    "📧 Email Intel (Lote)",
    "✉️ Gerador de Emails",
    "🧠 Briefing Estratégico",
    "📝 Gestor de Atas",
    "📈 Mercado & Churn",
    "📊 Relatório Master"
]
selected_module = st.selectbox("Seletor de Módulo", menu_list, label_visibility="collapsed")
st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# --- 7. MÓDULOS DE FUNCIONALIDADES INTEGRAIS (SEM CORTES) ---

if "🏠 Dashboard" in selected_module:
    st.markdown('<div class="main-card"><h1>Centro de Comando</h1><p>Monitoramento de integridade da Governança Cognitiva e Redundância.</p></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Motor IA", "Soberana", "Redundância On")
    with c2: st.metric("Operador", st.session_state.user_atual.capitalize(), "Autenticado")
    with c3: st.metric("Failover", "Ativo", "5 Camadas")

elif "📁 Analisador McKinsey" in selected_module:
    st.markdown('<div class="main-card"><h2>📁 Analisador de Documentos McKinsey</h2><p>Auditoria técnica e extração estratégica de valor com foco em mitigação de riscos.</p></div>', unsafe_allow_html=True)
    file = st.file_uploader("Documento (PDF/DOCX):", type=['pdf', 'docx'])
    if file and st.button("EXECUTAR AUDITORIA SÊNIOR"):
        with st.spinner("Analisando estrutura estratégica..."):
            p_mc = "Aja como McKinsey. Forneça: Resumo Executivo, Análise de Riscos, Impacto Financeiro/ROI e Plano de Ação 30-60-90."
            if file.type == "application/pdf":
                data_in = [{"mime_type": "application/pdf", "data": file.read()}]
            else:
                data_in = [file.read().decode(errors="ignore")]
            res, m_used = call_technobolt_ai(p_mc, data_in)
            st.markdown(f"<p style='font-size:10px; color:#64748b;'>Processado via: {m_used}</p>", unsafe_allow_html=True)
            st.markdown(res)
            st.download_button("📥 Baixar Relatório Corporativo", data=export_to_docx("Auditoria McKinsey", res), file_name="Auditoria.docx")

elif "📧 Email Intel" in selected_module:
    st.markdown('<div class="main-card"><h2>📧 Email Intel: Auditoria em Lote</h2><p>Análise massiva de e-mails em PDF para triagem estratégica.</p></div>', unsafe_allow_html=True)
    emails = st.file_uploader("Selecione os e-mails (PDF):", type=['pdf'], accept_multiple_files=True)
    if emails and st.button("PROCESSAR LOTE"):
        for email_pdf in emails:
            with st.expander(f"Auditoria: {email_pdf.name}", expanded=True):
                res, _ = call_technobolt_ai("Resuma tecnicamente e rascunhe a resposta executiva ideal.", [{"mime_type": "application/pdf", "data": email_pdf.read()}])
                st.markdown(res)

elif "✉️ Gerador de Emails" in selected_module:
    st.markdown('<div class="main-card"><h2>✉️ Gerador de Emails de Alto Impacto</h2></div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    my_role = col_a.text_input("Seu Cargo:")
    dest_role = col_b.text_input("Cargo do Destinatário:")
    email_objective = st.text_area("Objetivo Central da Mensagem:")
    if st.button("REDIGIR E-MAIL EXECUTIVO"):
        p_email = f"Como {my_role}, escreva um email para {dest_role} sobre {email_objective}. Use tom executivo de autoridade."
        res_email, _ = call_technobolt_ai(p_email)
        st.markdown(f'<div class="main-card">{res_email}</div>', unsafe_allow_html=True)
        st.download_button("📥 Baixar Word", data=export_to_docx("Rascunho de E-mail", res_email), file_name="Email.docx")

elif "🧠 Briefing" in selected_module:
    st.markdown('<div class="main-card"><h2>🧠 Briefing Estratégico & Radar 2026</h2></div>', unsafe_allow_html=True)
    company_target = st.text_input("Empresa ou Setor:")
    if st.button("ESCANEIA MERCADO"):
        res_brief, _ = call_technobolt_ai(f"Gere um briefing estratégico 2026 completo para {company_target}. Foco em concorrência, market share e riscos disruptivos.")
        st.markdown(res_brief)

elif "📝 Gestor de Atas" in selected_module:
    st.markdown('<div class="main-card"><h2>📝 Gestor de Atas de Governança</h2></div>', unsafe_allow_html=True)
    meeting_notes = st.text_area("Notas ou Transcrição da Reunião:", height=250)
    if st.button("FORMALIZAR ATA"):
        res_ata, _ = call_technobolt_ai(f"Formalize as seguintes notas em uma Ata de Diretoria Profissional: {meeting_notes}")
        st.markdown(f'<div class="main-card">{res_ata}</div>', unsafe_allow_html=True)
        st.download_button("📥 Baixar Ata Word", data=export_to_docx("Ata Oficial", res_ata), file_name="Ata_Oficial.docx")

elif "📈 Mercado & Churn" in selected_module:
    st.markdown('<div class="main-card"><h2>📈 Inteligência de Mercado & Churn</h2></div>', unsafe_allow_html=True)
    tab_rival, tab_churn = st.tabs(["🔍 Radar Concorrência", "⚠️ Risco de Churn"])
    with tab_rival:
        rival_name = st.text_input("Empresa Concorrente:")
        if st.button("ANALISAR ESTRATÉGIA"):
            res_rival, _ = call_technobolt_ai(f"Analise estrategicamente o posicionamento e ameaça de: {rival_name}")
            st.markdown(res_rival)
    with tab_churn:
        client_feed = st.text_area("Feedback do Cliente:")
        if st.button("CALCULAR RISCO"):
            res_churn, _ = call_technobolt_ai(f"Avalie o risco de churn (perda) baseado neste feedback: {client_feed}")
            st.markdown(res_churn)

elif "📊 Relatório Master" in selected_module:
    st.markdown('<div class="main-card"><h2>📊 Relatório Master de Diretoria</h2></div>', unsafe_allow_html=True)
    weekly_data = st.text_area("Fatos e KPIs da Semana:")
    if st.button("GERAR DOSSIÊ MASTER"):
        res_master, _ = call_technobolt_ai(f"Gere um Relatório Master de Governança consolidando: {weekly_data}. Foco em impacto executivo.")
        st.markdown(res_master)
        st.download_button("📥 Baixar Master", data=export_to_docx("Relatório Master", res_master), file_name="Master.docx")

# --- 8. CHATBOT POPUP LATERAL (ASSISTENTE DE ONBOARDING) ---



st.markdown("""
    <div style="position: fixed; bottom: 30px; right: 30px; z-index: 10001;">
        <button style="background:#1e40af; border:none; width:65px; height:65px; border-radius:50%; box-shadow: 0 10px 30px rgba(0,0,0,0.1); color:white; font-size:28px; cursor:pointer;">💡</button>
    </div>
""", unsafe_allow_html=True)

with st.container():
    col_side, col_chat_box = st.columns([4, 1.2])
    with col_chat_box:
        if st.checkbox("Assistente de Módulos", key="check_onboarding"):
            st.markdown('<div class="chat-popup"><div class="chat-header">Guia de Soluções</div>', unsafe_allow_html=True)
            st.markdown("<div style='padding:20px;'>", unsafe_allow_html=True)
            mod_to_explain = st.selectbox("Explique como funciona o módulo:", menu_list, key="sel_expl")
            if st.button("SOLICITAR EXPLICAÇÃO"):
                explanation = call_technobolt_ai(f"Explique detalhadamente como o módulo '{mod_to_explain}' funciona e quais benefícios ele gera para o usuário corporativo.", mode_explainer=True)[0]
                st.info(explanation)
            st.markdown("</div></div>", unsafe_allow_html=True)

# --- RODAPÉ DE SEGURANÇA ---
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
st.caption(f"TechnoBolt Solutions © 2026 | Elite Hub Edition v1.0 | Licenciado para: {st.session_state.user_atual.upper()}")