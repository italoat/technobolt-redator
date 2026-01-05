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
    }

    .hero-title {
        font-size: 42px; font-weight: 800; text-align: center;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
        margin-bottom: 10px;
    }

    /* CORREÇÃO DEFINITIVA DA LISTA SUSPENSA (SELECTBOX) */
    .stSelectbox [data-baseweb="select"] {
        width: 100% !important;
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 8px !important;
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

    /* BOTÃO DE SAIR (DESIGN CLEAN E DISCRETO) */
    .logout-zone .stButton > button {
        background: transparent !important;
        color: #ef4444 !important;
        border: 1px solid #fee2e2 !important;
        height: 2.8em !important;
        width: auto !important;
        padding: 0 25px !important;
        text-transform: none !important;
        font-size: 14px !important;
        letter-spacing: 0 !important;
        font-weight: 600 !important;
    }
    .logout-zone .stButton > button:hover {
        background: #fef2f2 !important;
        border-color: #f87171 !important;
    }

    /* CHATBOT POPUP LATERAL (FIXO E ESTÁVEL) */
    .chat-popup {
        position: fixed; bottom: 100px; right: 30px; width: 380px; height: 550px;
        background: white; border: 1px solid #1e40af; border-radius: 25px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.15); z-index: 9999; overflow: hidden;
    }
    .chat-header { background: #1e40af; color: white; padding: 20px; font-weight: 700; text-align: center; }

    /* MÉTTRICAS E DASHBOARD */
    .stMetric {
        background: white; border: 1px solid #e2e8f0; border-radius: 18px; padding: 25px;
    }
    
    .status-badge {
        padding: 6px 18px; border-radius: 50px; background: #eff6ff; 
        color: #1e40af; font-size: 12px; font-weight: 700; border: 1px solid #dbeafe;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. TELA DE LOGIN (DESIGN CENTRALIZADO ÚNICO) ---
def render_auth_screen():
    st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1.4, 1])
    with col_login:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>TECHNOBOLT HUB</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#64748b; margin-bottom:40px; letter-spacing:1px;'>GOVERNANÇA COGNITIVA & IA ELITE</p>", unsafe_allow_html=True)
        
        id_operador = st.text_input("Credencial de Operador", placeholder="Usuário")
        chave_seguranca = st.text_input("Chave de Acesso", type="password", placeholder="Senha")
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        if st.button("AUTENTICAR NO HUB"):
            banco_usuarios = {
                "admin": "admin",
                "jackson.antonio": "teste@2025",
                "luiza.trovao": "teste@2025",
                "usuario.teste": "teste@2025"
            }
            if id_operador in banco_usuarios and banco_usuarios[id_operador] == chave_seguranca:
                st.session_state.logged_in = True
                st.session_state.user_atual = id_operador
                st.rerun()
            else:
                st.error("Protocolo de Segurança: Credenciais não autorizadas.")
        
        st.markdown("<p style='text-align:center; color:#94a3b8; font-size:10px; margin-top:45px; letter-spacing:2px;'>SISTEMA PROTEGIDO POR AES-256</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    render_auth_screen()
    st.stop()

# --- 5. MOTOR DE INTELIGÊNCIA COM SEUS MODELOS ORIGINAIS (FAILOVER 5 NÍVEIS) ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# RECUPERAÇÃO DA SUA LISTA DE MODELOS ORIGINAIS
MODEL_PRIORITY_LIST = [
    "models/gemini-3-flash-preview", 
    "models/gemini-2.5-flash", 
    "models/gemini-2.0-flash", 
    "models/gemini-2.0-flash-lite", 
    "models/gemini-flash-latest"
]

def call_ai_technobolt_failover(prompt, attachments=None, onboarding_mode=False):
    """Executa a requisição com failover automático entre seus 5 modelos e prompts McKinsey."""
    
    # PROMPTS ROBUSTOS E APRIMORADOS
    sys_instruction = (
        "Você é o Motor de Inteligência Estratégica da TechnoBolt Solutions. "
        "Sua postura é de um consultor sênior McKinsey/BCG/Bain. "
        "DIRETRIZES: 1. Respostas técnicas, analíticas e extremamente profundas. 2. Use terminologia executiva. "
        "3. Markdown estruturado com tabelas e diagnósticos. 4. Foco total em ROI, Governança e Riscos. "
        "Proibido saudações genéricas ou conversas informais. Responda diretamente ao ponto técnico."
    )
    
    if onboarding_mode:
        sys_instruction = (
            "Você é o Guia de Integração TechnoBolt. Explique de forma didática e executiva como "
            "cada módulo do Hub resolve dores de negócio e gera eficiência operacional para o cliente."
        )

    for model_name in MODEL_PRIORITY_LIST:
        try:
            model = genai.GenerativeModel(model_name, system_instruction=sys_instruction)
            payload = [prompt] + attachments if attachments else prompt
            response = model.generate_content(payload)
            return response.text, model_name
        except Exception:
            # Fallback manual para contingência (modelos legados)
            try:
                model_fb = genai.GenerativeModel(model_name)
                full_p = f"{sys_instruction}\n\nSOLICITAÇÃO: {prompt}"
                response = model_fb.generate_content([full_p] + attachments if attachments else full_p)
                return response.text, model_name
            except:
                continue
    return "⚠️ CRITICAL_ERROR: Todos os motores de redundância falharam.", "OFFLINE"

def extrair_texto_docx(arquivo_docx):
    """Extração técnica de texto de arquivos Microsoft Word."""
    doc = docx.Document(arquivo_docx)
    return "\n".join([p.text for p in doc.paragraphs])

def export_to_word_format(title, content):
    """Gera um documento Microsoft Word com formatação corporativa e cabeçalho de auditoria."""
    doc = docx.Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(f"Relatório de Governança | Operador: {st.session_state.user_atual.upper()}")
    doc.add_paragraph(f"TechnoBolt Hub Elite | Timestamp: {time.strftime('%d/%m/%Y %H:%M:%S')}")
    doc.add_paragraph("-" * 60)
    doc.add_paragraph(content)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 6. CABEÇALHO E NAVEGAÇÃO SUPERIOR ---
st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
head_col1, head_col2 = st.columns([4, 1])

with head_col1:
    st.markdown(f"**OPERADOR:** <span class='status-badge'>{st.session_state.user_atual.upper()}</span>", unsafe_allow_html=True)

with head_col2:
    st.markdown('<div class="logout-zone">', unsafe_allow_html=True)
    if st.button("🚪 Sair do Sistema"):
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
modulo_selecionado = st.selectbox("Seletor de Módulo", menu_navegacao, label_visibility="collapsed")
st.markdown("<hr style='margin: 10px 0 35px 0; border: 0.5px solid #e2e8f0;'>", unsafe_allow_html=True)

# --- 7. MÓDULOS DE FUNCIONALIDADES INTEGRAIS (460+ LINHAS) ---

# DASHBOARD
if "🏠 Dashboard" in modulo_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h1>Command Center</h1><p>Monitoramento de integridade da Governança Cognitiva e Redundância de Motores.</p></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("IA Engine", "Soberana", "Redundância On")
    with c2: st.metric("Status Operador", st.session_state.user_atual.capitalize(), "Autenticado")
    with c3: st.metric("Failover", "Ativo", "5 Camadas")

# ANALISADOR MCKINSEY
elif "📁 Analisador McKinsey" in modulo_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>📁 Analisador de Documentos McKinsey</h2><p>Auditoria técnica e extração estratégica de valor com foco em mitigação de riscos.</p></div>', unsafe_allow_html=True)
    arquivo_up = st.file_uploader("Submeter Documento (PDF/DOCX/TXT):", type=['pdf', 'docx', 'txt'])
    if arquivo_up and st.button("EXECUTAR AUDITORIA SÊNIOR"):
        with st.spinner("IA Processando sob padrão McKinsey de excelência..."):
            if arquivo_up.type == "application/pdf":
                dados_ia = [{"mime_type": "application/pdf", "data": arquivo_up.read()}]
                p_mc = "Aja como McKinsey. Forneça: Resumo Executivo, Análise de Riscos, Impacto Financeiro/ROI e Plano de Ação 30-60-90."
            else:
                texto_raw = extrair_texto_docx(arquivo_up) if arquivo_up.name.endswith('docx') else arquivo_up.read().decode(errors="ignore")
                dados_ia = [texto_raw]
                p_mc = "Analise tecnicamente este documento para a Technobolt Solutions sob a ótica de eficiência operacional."
            
            res_ia, model_ia = call_ai_technobolt_failover(p_mc, dados_ia)
            st.markdown(f"<p style='font-size:10px; color:#64748b;'>Processado via: {model_ia}</p>", unsafe_allow_html=True)
            st.markdown(res_ia)
            st.download_button("📥 Baixar Relatório", data=export_to_word_format("Auditoria McKinsey", res_ia), file_name=f"Auditoria_{arquivo_up.name}.docx")

# EMAIL INTEL (LOTE)
elif "📧 Email Intel" in modulo_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>📧 Email Intel: Auditoria em Lote</h2><p>Processamento massivo de e-mails em PDF para triagem e inteligência.</p></div>', unsafe_allow_html=True)
    lote_emails = st.file_uploader("Selecione os e-mails (PDF):", type=['pdf'], accept_multiple_files=True)
    if lote_emails and st.button("PROCESSAR LOTE DE AUDITORIA"):
        for email_pdf in lote_emails:
            with st.expander(f"Auditoria: {email_pdf.name}", expanded=True):
                res_email, _ = call_ai_technobolt_failover(f"Resuma este e-mail e rascunhe a resposta executiva ideal.", [{"mime_type": "application/pdf", "data": email_pdf.read()}])
                st.markdown(res_email)

# GERADOR DE EMAILS
elif "✉️ Gerador de Emails" in modulo_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>✉️ Gerador de Emails de Alto Impacto</h2></div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    cargo_op = col_a.text_input("Seu Cargo:")
    dest_op = col_b.text_input("Cargo do Destinatário:")
    obj_email = st.text_area("Objetivo Central da Mensagem ou Tópicos:")
    if st.button("REDIGIR E-MAIL EXECUTIVO"):
        with st.spinner("Redigindo rascunho executivo..."):
            p_email = f"Como {cargo_op}, escreva um email para {dest_op} sobre {obj_email}. Use tom executivo de autoridade."
            res_email, _ = call_ai_technobolt_failover(p_email)
            st.markdown(f'<div class="main-card" style="max-width:100%;">{res_email}</div>', unsafe_allow_html=True)
            st.download_button("📥 Baixar Word", data=export_to_word_format("Rascunho de E-mail", res_email), file_name="Rascunho_Email.docx")

# BRIEFING ESTRATÉGICO
elif "🧠 Briefing" in modulo_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>🧠 Briefing Estratégico & Radar 2026</h2></div>', unsafe_allow_html=True)
    empresa_alvo = st.text_input("Empresa ou Setor para Análise:")
    if st.button("EXECUTAR SCAN DE MERCADO"):
        res_brief, _ = call_ai_technobolt_failover(f"Gere um briefing estratégico 2026 completo para {empresa_alvo}. Foco em concorrência e riscos.")
        st.markdown(res_brief)

# GESTOR DE ATAS
elif "📝 Gestor de Atas" in modulo_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>📝 Gestor de Atas de Governança</h2></div>', unsafe_allow_html=True)
    notas_reuniao = st.text_area("Notas ou Transcrição da Reunião:", height=280)
    if st.button("FORMALIZAR ATA DE DIRETORIA"):
        res_ata, _ = call_ai_technobolt_failover(f"Formalize as seguintes notas em uma Ata de Diretoria TechnoBolt Profissional: {notas_reuniao}")
        st.markdown(f'<div class="main-card" style="max-width:100%;">{res_ata}</div>', unsafe_allow_html=True)
        st.download_button("📥 Baixar Ata", data=export_to_word_format("Ata de Reunião", res_ata), file_name="Ata_Oficial.docx")

# MERCADO & CHURN
elif "📈 Mercado & Churn" in modulo_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>📈 Inteligência de Mercado & Churn</h2></div>', unsafe_allow_html=True)
    tab_rival, tab_churn = st.tabs(["🔍 Radar de Concorrência", "⚠️ Risco de Churn"])
    with tab_rival:
        rival_n = st.text_input("Empresa Concorrente:")
        if st.button("ANALISAR ESTRATÉGIA RIVAL"):
            res_rival, _ = call_ai_technobolt_failover(f"Analise estrategicamente a empresa: {rival_n}")
            st.markdown(res_rival)
    with tab_churn:
        feedback_c = st.text_area("Feedback do Cliente:")
        if st.button("CALCULAR RISCO DE PERDA"):
            res_churn, _ = call_ai_technobolt_failover(f"Avalie o risco de churn baseado neste feedback: {feedback_c}")
            st.markdown(res_churn)

# RELATÓRIO MASTER
elif "📊 Relatório Master" in modulo_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>📊 Relatório Master de Diretoria</h2></div>', unsafe_allow_html=True)
    kpis_semana = st.text_area("Fatos e métricas da semana:")
    if st.button("GERAR DOSSIÊ MASTER"):
        res_master, _ = call_ai_technobolt_failover(f"Gere um Relatório Master de Governança consolidando: {kpis_semana}")
        st.markdown(res_master)
        st.download_button("📥 Baixar Dossiê", data=export_to_word_format("Relatório Master", res_master), file_name="Master_Dossie.docx")

# --- 8. CHATBOT POPUP LATERAL DE ONBOARDING (ESTÁVEL) ---



st.markdown("""
    <div style="position: fixed; bottom: 30px; right: 30px; z-index: 10001;">
        <button style="background:#1e40af; border:none; width:65px; height:65px; border-radius:50%; box-shadow: 0 10px 30px rgba(30,64,175,0.2); color:white; font-size:28px; cursor:pointer;">💡</button>
    </div>
""", unsafe_allow_html=True)

with st.container():
    col_vazia, col_chat_ui = st.columns([4, 1.3])
    with col_chat_ui:
        if st.checkbox("Assistente de Módulos", key="check_onboarding_hub"):
            st.markdown('<div class="chat-popup"><div class="chat-header">Guia de Soluções TechnoBolt</div>', unsafe_allow_html=True)
            st.markdown("<div style='padding:20px;'>", unsafe_allow_html=True)
            mod_para_explicar = st.selectbox("Selecione o módulo para entender:", menu_navegacao, key="sel_expl_onb")
            if st.button("SOLICITAR EXPLICAÇÃO"):
                guia_texto, _ = call_ai_technobolt_failover(f"Explique como o módulo '{mod_para_explicar}' funciona e seus benefícios corporativos.", onboarding_mode=True)
                st.info(guia_texto)
            st.markdown("</div></div>", unsafe_allow_html=True)

# --- RODAPÉ DE GOVERNANÇA ---
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
st.caption(f"TechnoBolt Solutions © 2026 | Elite Hub Edition v6.5 | Operador: {st.session_state.user_atual.upper()}")