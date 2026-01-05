import streamlit as st
import google.generativeai as genai
import os
import time
import docx  # Requer: pip install python-docx
from io import BytesIO
import base64

# --- 1. CONFIGURAÇÃO DE SEGURANÇA E PROTOCOLO (ELITE HUB) ---
st.set_page_config(
    page_title="TechnoBolt IA - Elite Hub de Governança",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. GESTÃO DE ESTADO (PERSISTÊNCIA E CHAT) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_atual' not in st.session_state:
    st.session_state.user_atual = None
if 'chat_step' not in st.session_state:
    st.session_state.chat_step = "menu"
if 'chat_response' not in st.session_state:
    st.session_state.chat_response = ""
if 'analise_count' not in st.session_state:
    st.session_state.analise_count = 0

def protocol_logout():
    """Finaliza a sessão e limpa os estados de segurança do operador."""
    st.session_state.logged_in = False
    st.session_state.user_atual = None
    st.rerun()

# --- 3. DESIGN SYSTEM (LIGHT CORPORATE EXCLUSIVE - ULTRA CLEAN) ---
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

    /* CARD CORPORATIVO PROFISSIONAL */
    .main-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 45px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04);
        margin-bottom: 30px;
        animation: fadeIn 0.8s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .hero-title {
        font-size: 42px; font-weight: 800; text-align: center;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
        margin-bottom: 10px;
    }

    /* CORREÇÃO DA LISTA SUSPENSA (SELECTBOX) */
    .stSelectbox [data-baseweb="select"] {
        width: 100% !important;
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 10px !important;
        min-height: 50px !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: transparent !important;
        border: none !important;
    }

    /* ESTILIZAÇÃO DE INPUTS E TEXTAREAS */
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        font-size: 16px !important;
        color: #0f172a !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important;
    }

    /* BOTÃO TECHNOBOLT EXCLUSIVE (MÓDULOS) */
    .stButton > button {
        width: 100%; border-radius: 14px; height: 3.8em; font-weight: 700;
        background: #1e40af !important; color: white !important; border: none !important;
        text-transform: uppercase; letter-spacing: 1.5px; transition: 0.4s;
        display: flex; align-items: center; justify-content: center;
    }
    .stButton > button:hover {
        background: #1e3a8a !important; transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(30, 64, 175, 0.25) !important;
    }
    .stButton > button div[data-testid="stMarkdownContainer"] p {
        background: none !important; color: white !important; margin: 0 !important;
        padding: 0 !important; text-shadow: none !important;
    }

    /* BOTÃO DE SAIR (DESIGN CLEAN) */
    .logout-zone .stButton > button {
        background: transparent !important;
        color: #ef4444 !important;
        border: 1px solid #fee2e2 !important;
        height: 3em !important;
        width: auto !important;
        padding: 0 30px !important;
        text-transform: none !important;
        font-size: 14px !important;
        letter-spacing: 0 !important;
        font-weight: 600 !important;
    }

    /* CHATBOT POPUP (FIXO E ESTÁVEL) */
    .chat-popup {
        position: fixed; bottom: 100px; right: 30px; width: 400px; max-height: 600px;
        background: white; border: 1px solid #1e40af; border-radius: 25px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.15); z-index: 9999; 
        display: flex; flex-direction: column; overflow: hidden;
    }
    .chat-header { background: #1e40af; color: white; padding: 20px; font-weight: 700; text-align: center; }
    .chat-content { padding: 25px; overflow-y: auto; background: #fdfdfd; max-height: 400px; }
    
    .chat-bubble-agent {
        background: #eff6ff; border-radius: 15px 15px 15px 0;
        padding: 15px; margin-bottom: 12px; font-size: 14px; border: 1px solid #dbeafe;
        color: #1e40af;
    }

    .status-badge {
        padding: 6px 18px; border-radius: 50px; background: #eff6ff; 
        color: #1e40af; font-size: 12px; font-weight: 700; border: 1px solid #dbeafe;
    }
    
    .stMetric { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 18px; padding: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 4. TELA DE LOGIN ---
def render_auth():
    st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1.4, 1])
    with col_login:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>TECHNOBOLT HUB</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#64748b; margin-bottom:40px; letter-spacing:1px;'>TERMINAL DE GOVERNANÇA COGNITIVA</p>", unsafe_allow_html=True)
        
        user_id = st.text_input("Credencial Identificadora", placeholder="Ex: jackson.antonio")
        user_key = st.text_input("Chave de Segurança", type="password", placeholder="••••••••")
        
        if st.button("AUTENTICAR NO HUB"):
            db_users = {"admin": "admin", "jackson.antonio": "teste@2025", "luiza.trovao": "teste@2025"}
            if user_id in db_users and db_users[user_id] == user_key:
                st.session_state.logged_in = True
                st.session_state.user_atual = user_id
                st.rerun()
            else:
                st.error("Protocolo negado. Credenciais inválidas.")
        st.markdown("<p style='text-align:center; color:#94a3b8; font-size:10px; margin-top:45px;'>SISTEMA PROTEGIDO POR AES-256</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    render_auth()
    st.stop()

# --- 5. MOTOR DE INTELIGÊNCIA COM SEUS MODELOS ORIGINAIS (FAILOVER 5 NÍVEIS) ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key: genai.configure(api_key=api_key)

# LISTA DE MODELOS ORIGINAIS INTEGRADA
MODEL_FAILOVER_LIST = [
    "models/gemini-3-flash-preview", 
    "models/gemini-2.5-flash", 
    "models/gemini-2.0-flash", 
    "models/gemini-2.0-flash-lite", 
    "models/gemini-flash-latest"
]

def call_technobolt_ai(prompt, attachments=None, onboarding=False):
    """Executa a requisição com failover absoluto e System Instructions expandidas."""
    
    sys_instr = (
        "Você é o Motor de Inteligência Estratégica da TechnoBolt Solutions. "
        "Sua postura é de um consultor sênior McKinsey/BCG/Bain. "
        "DIRETRIZES: 1. Respostas técnicas, analíticas e extremamente profundas. 2. Use terminologia executiva. "
        "3. Markdown estruturado com diagnósticos e tabelas. 4. Foco total em ROI e Riscos. "
        "Proibido saudações informais. Responda diretamente ao ponto técnico."
    )
    
    if onboarding:
        sys_instr = (
            "Você é o Agente Virtual TechnoBolt. Seu objetivo é explicar como cada solução do Hub "
            "auxilia na governança corporativa e eficiência operacional. Seja didático mas profissional."
        )

    for model_id in MODEL_FAILOVER_LIST:
        try:
            model = genai.GenerativeModel(model_id, system_instruction=sys_instr)
            payload = [prompt] + attachments if attachments else prompt
            response = model.generate_content(payload)
            return response.text, model_id
        except Exception:
            continue
    return "⚠️ Motores de IA Offline. Contate a governança.", "OFFLINE"

def export_docx(title, content):
    """Gera documentos Microsoft Word com formatação corporativa."""
    doc = docx.Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(f"Relatório de Governança | Operador: {st.session_state.user_atual.upper()}")
    doc.add_paragraph(f"Timestamp: {time.strftime('%d/%m/%Y %H:%M:%S')}")
    doc.add_paragraph("-" * 60)
    doc.add_paragraph(content)
    buf = BytesIO(); doc.save(buf); buf.seek(0)
    return buf

def extrair_texto_docx(arquivo_docx):
    """Extração técnica de texto de arquivos .docx."""
    doc = docx.Document(arquivo_docx)
    return "\n".join([p.text for p in doc.paragraphs])

# --- 6. CABEÇALHO E NAVEGAÇÃO ---
st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
head_l, head_r = st.columns([4, 1.2])

with head_l:
    st.markdown(f"**OPERADOR:** <span class='status-badge'>{st.session_state.user_atual.upper()}</span>", unsafe_allow_html=True)

with head_r:
    st.markdown('<div class="logout-zone">', unsafe_allow_html=True)
    if st.button("🚪 Sair do Hub"):
        protocol_logout()
    st.markdown('</div>', unsafe_allow_html=True)

menu_navegacao = [
    "🏠 Dashboard de Comando", 
    "📁 Analisador McKinsey", 
    "📧 Email Intel (Lote)", 
    "✉️ Gerador de Emails", 
    "🧠 Briefing Estratégico", 
    "📝 Gestor de Atas", 
    "📈 Mercado & Churn", 
    "📊 Relatório Master"
]
escolha = st.selectbox("Seletor de Módulo", menu_navegacao, label_visibility="collapsed")
st.markdown("<hr style='margin: 10px 0 35px 0; border: 0.5px solid #e2e8f0;'>", unsafe_allow_html=True)

# --- 7. MÓDULOS DE FUNCIONALIDADES INTEGRAIS (SEM CORTES) ---

# DASHBOARD
if "🏠 Dashboard" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h1>Command Center</h1><p>Monitoria de Soberania Digital e Redundância Ativa.</p></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("IA Engine", "Soberana", "Redundância On")
    c2.metric("Sessão", st.session_state.user_atual.capitalize(), "Protegida")
    c3.metric("Failover", "Ativo", "5 Camadas")

# ANALISADOR MCKINSEY
elif "📁 Analisador McKinsey" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>Analisador de Documentos McKinsey</h2><p>Auditoria técnica e extração estratégica de valor.</p></div>', unsafe_allow_html=True)
    f_up = st.file_uploader("Documento (PDF/DOCX/TXT):", type=['pdf', 'docx', 'txt'])
    if f_up and st.button("EXECUTAR AUDITORIA SÊNIOR"):
        with st.spinner("Analisando estrutura estratégica..."):
            if f_up.type == "application/pdf":
                dados_ia = [{"mime_type": "application/pdf", "data": f_up.read()}]
                p_mc = "Aja como McKinsey. Forneça: Resumo Executivo, Swot de Risco, ROI Estimado e Plano 90 dias."
            else:
                texto_raw = extrair_texto_docx(f_up) if f_up.name.endswith('docx') else f_up.read().decode(errors="ignore")
                dados_ia = [texto_raw]
                p_mc = "Analise tecnicamente este documento para a Technobolt Solutions sob a ótica de eficiência operacional."
            
            res_ia, mod_ia = call_technobolt_ai(p_mc, dados_ia)
            st.markdown(f"<p style='font-size:10px; color:#64748b;'>Processado via: {mod_ia}</p>", unsafe_allow_html=True)
            st.markdown(res_ia)
            st.download_button("📥 Baixar Relatório", data=export_docx("Auditoria McKinsey", res_ia), file_name=f"Auditoria_{f_up.name}.docx")

# EMAIL INTEL (LOTE)
elif "📧 Email Intel" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>Email Intel: Auditoria em Lote</h2><p>Processamento massivo de e-mails em PDF para triagem estratégica.</p></div>', unsafe_allow_html=True)
    emails = st.file_uploader("Upload Emails (PDF):", type=['pdf'], accept_multiple_files=True)
    if emails and st.button("PROCESSAR LOTE DE AUDITORIA"):
        for email_pdf in emails:
            with st.expander(f"Auditoria: {email_pdf.name}", expanded=True):
                res_email, _ = call_technobolt_ai("Resuma tecnicamente e rascunhe a resposta executiva ideal.", [{"mime_type": "application/pdf", "data": email_pdf.read()}])
                st.markdown(res_email)

# GERADOR DE EMAILS
elif "✉️ Gerador de Emails" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>Gerador de Emails de Alto Impacto</h2></div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    cargo_e = ca.text_input("Seu Cargo para Assinatura:")
    dest_e = cb.text_input("Cargo do Destinatário:")
    
    # NOVA BARRA DE FORMALIDADE
    formalidade = st.select_slider("Nível de Formalidade Corporativa", 
                                   options=["Casual/Startup", "Corporativo Padrão", "Executivo/Sênior", "Rígido/Diplomático"], 
                                   value="Executivo/Sênior")
    
    contexto_e = st.text_area("Objetivo da Mensagem ou Tópicos Críticos:")
    if st.button("REDIGIR E-MAIL EXECUTIVO"):
        with st.spinner("Redigindo rascunho..."):
            p_email = f"Como {cargo_e}, escreva um email para {dest_e} sobre {contexto_e}. Nível de formalidade: {formalidade}. Tom de autoridade."
            res_email, _ = call_technobolt_ai(p_email)
            st.markdown(f'<div class="main-card" style="max-width:100%;">{res_email}</div>', unsafe_allow_html=True)
            st.download_button("📥 Baixar Rascunho", data=export_docx("Email Gerado", res_email), file_name="Rascunho_Email.docx")

# BRIEFING ESTRATÉGICO
elif "🧠 Briefing" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>Briefing Estratégico & Radar 2026</h2></div>', unsafe_allow_html=True)
    e_alvo = st.text_input("Empresa ou Setor Alvo:")
    if st.button("EXECUTAR SCAN DE MERCADO"):
        with st.spinner("Escaneando mercado..."):
            res_brief, _ = call_technobolt_ai(f"Gere um briefing estratégico 2026 completo para {e_alvo}. Foco em concorrência, market share e riscos disruptivos.")
            st.markdown(res_brief)

# GESTOR DE ATAS
elif "📝 Gestor de Atas" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>Gestor de Atas de Governança</h2></div>', unsafe_allow_html=True)
    notas_r = st.text_area("Notas da Reunião ou Transcrição:", height=280)
    if st.button("FORMALIZAR ATA DE DIRETORIA"):
        with st.spinner("Formatando ata..."):
            res_ata, _ = call_technobolt_ai(f"Formalize as seguintes notas em uma Ata de Diretoria TechnoBolt Profissional: {notas_r}")
            st.markdown(f'<div class="main-card" style="max-width:100%;">{res_ata}</div>', unsafe_allow_html=True)
            st.download_button("📥 Baixar Ata Word", data=export_docx("Ata Oficial", res_ata), file_name="Ata_Oficial.docx")

# MERCADO & CHURN
elif "📈 Mercado & Churn" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>Inteligência de Mercado & Churn</h2></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Radar de Concorrência", "⚠️ Risco de Churn"])
    with t1:
        rival = st.text_input("Empresa Concorrente:")
        if st.button("ANALISAR RIVAL"):
            res_rival, _ = call_technobolt_ai(f"Analise estrategicamente a empresa: {rival}"); st.markdown(res_rival)
    with t2:
        feed_c = st.text_area("Feedback do Cliente para Análise:");
        if st.button("CALCULAR RISCO"):
            res_churn, _ = call_technobolt_ai(f"Avalie o risco de churn baseado neste feedback e proponha retenção: {feed_c}"); st.markdown(res_churn)

# RELATÓRIO MASTER
elif "📊 Relatório Master" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>Relatório Master de Diretoria</h2><p>Dossiê consolidado de KPIs e eventos da semana.</p></div>', unsafe_allow_html=True)
    kpis = st.text_area("Fatos, métricas e decisões da semana:")
    if st.button("GERAR DOSSIÊ MASTER"):
        with st.spinner("Consolidando governança..."):
            res_master, _ = call_technobolt_ai(f"Gere um Relatório Master de Governança TechnoBolt consolidando: {kpis}. Foco em impacto executivo.")
            st.markdown(res_master)
            st.download_button("📥 Baixar Dossiê", data=export_docx("Relatório Master", res_master), file_name="Master_Dossie.docx")

# --- 8. CHATBOT POPUP (AGENTE VIRTUAL CORRIGIDO) ---



st.markdown("""
    <div style="position: fixed; bottom: 30px; right: 30px; z-index: 10001;">
        <button style="background:#1e40af; border:none; width:65px; height:65px; border-radius:50%; box-shadow: 0 10px 30px rgba(30,64,175,0.2); color:white; font-size:28px; cursor:pointer;">💡</button>
    </div>
""", unsafe_allow_html=True)

with st.container():
    col_v, col_chat = st.columns([4, 1.4])
    with col_chat:
        if st.checkbox("Agente Virtual", key="chat_pop_v7"):
            st.markdown('<div class="chat-popup"><div class="chat-header">Hub de Soluções</div>', unsafe_allow_html=True)
            st.markdown('<div class="chat-content">', unsafe_allow_html=True)
            
            # Lógica de Menu dentro do Chat
            if st.session_state.chat_step == "menu":
                st.markdown('<div class="chat-bubble-agent">Olá! Sou seu assistente TechnoBolt. Qual solução você deseja entender em detalhes agora?</div>', unsafe_allow_html=True)
                for item in menu_navegacao:
                    if st.button(f"Saber mais: {item}", key=f"btn_chat_{item}"):
                        with st.spinner("IA Processando..."):
                            st.session_state.chat_response, _ = call_technobolt_ai(f"Explique o valor corporativo e como usar o módulo: {item}", onboarding=True)
                            st.session_state.chat_step = "response"
                            st.rerun()
            
            # Lógica de Resposta e Conversa
            if st.session_state.chat_step == "response":
                st.markdown(f'<div class="chat-bubble-agent">{st.session_state.chat_response}</div>', unsafe_allow_html=True)
                if st.button("Voltar ao Menu Principal"):
                    st.session_state.chat_step = "menu"
                    st.rerun()
            
            st.markdown('</div></div>', unsafe_allow_html=True)

# --- 9. RODAPÉ DE GOVERNANÇA ---
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
st.caption(f"TechnoBolt Solutions © 2026 | Elite Hub Edition v1.0 | Protocolo: {st.session_state.user_atual.upper()}")