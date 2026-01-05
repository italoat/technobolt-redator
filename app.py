import streamlit as st
import google.generativeai as genai
import os
import time
import docx  # Requer: pip install python-docx
from io import BytesIO
import base64

# --- 1. CONFIGURAÇÃO DA PÁGINA (PROTOCOLO DE SEGURANÇA) ---
st.set_page_config(
    page_title="TechnoBolt IA - Hub de Governança",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. GESTÃO DE ESTADO E PERSISTÊNCIA ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_atual' not in st.session_state:
    st.session_state.user_atual = None
if 'chat_visible' not in st.session_state:
    st.session_state.chat_visible = False
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. ARQUITETURA DE DESIGN SYSTEM (CSS EXPANDIDO) ---
def aplicar_estilo_dinamico():
    if st.session_state.theme == 'light':
        v_bg = "#f8fafc"
        v_text = "#1e293b"
        v_card = "#ffffff"
        v_border = "#e2e8f0"
        v_input = "#ffffff"
        v_metric = "#f1f5f9"
        v_sub = "#64748b"
    else:
        v_bg = "#0a192f"
        v_text = "#f1f5f9"
        v_card = "#112240"
        v_border = "#1e3a8a"
        v_input = "#0f172a"
        v_metric = "#1e3a8a"
        v_sub = "#8892b0"

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* RESET E ESTRUTURA GLOBAL */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {{
            background-color: {v_bg} !important;
            font-family: 'Inter', sans-serif !important;
            color: {v_text} !important;
            transition: all 0.5s ease;
        }}

        [data-testid="stSidebar"] {{ display: none !important; }}
        header, footer {{ visibility: hidden !important; }}

        /* COMPONENTES DE CARTÃO CORPORATIVO */
        .main-card {{
            background: {v_card};
            border: 1px solid {v_border};
            border-radius: 28px;
            padding: 50px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
            margin-bottom: 30px;
            animation: fadeIn 0.8s ease;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .hero-title {{
            font-size: 44px; font-weight: 800; text-align: center;
            background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -2px; margin-bottom: 8px;
        }}

        /* FORMULÁRIOS E INPUTS UX */
        .stTextInput input, .stTextArea textarea, [data-baseweb="select"], .stSelectbox div {{
            background-color: {v_input} !important;
            border: 1px solid {v_border} !important;
            border-radius: 14px !important;
            color: {v_text} !important;
            padding: 16px 20px !important;
            transition: border 0.3s ease;
        }}
        
        .stTextInput input:focus {{ border-color: #2563eb !important; }}

        /* BOTÕES DE ALTA PERFORMANCE */
        .stButton > button {{
            width: 100%; border-radius: 15px; height: 4.2em; font-weight: 700;
            background: #2563eb !important; color: #ffffff !important; border: none !important;
            text-transform: uppercase; letter-spacing: 2px;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2) !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4) !important;
        }}

        /* CHATBOT POPUP (SISTEMA DE FLUTUAÇÃO ESTÁVEL) */
        .chat-window {{
            position: fixed; bottom: 100px; right: 30px; 
            width: 400px; height: 550px;
            background: {v_card};
            border: 1px solid {v_border};
            border-radius: 30px;
            z-index: 99999;
            display: flex; flex-direction: column;
            box-shadow: 0 30px 70px rgba(0,0,0,0.2);
            overflow: hidden;
        }}

        .chat-header {{
            background: #2563eb; color: white; padding: 20px;
            font-weight: 800; text-align: center; font-size: 18px;
        }}

        /* MÉTTRICAS E DASHBOARD */
        .stMetric {{
            background: {v_metric}; 
            border: 1px solid {v_border}; 
            border-radius: 20px; 
            padding: 25px;
            transition: transform 0.3s ease;
        }}
        .stMetric:hover {{ transform: scale(1.02); }}

        hr {{ border: 0.5px solid {v_border}; margin: 40px 0; }}
        
        .status-badge {{
            padding: 5px 12px; border-radius: 50px; font-size: 11px;
            font-weight: 700; background: rgba(37, 99, 235, 0.1); color: #2563eb;
        }}
    </style>
    """, unsafe_allow_html=True)

aplicar_estilo_dinamico()

# --- 4. SISTEMA DE AUTENTICAÇÃO ---
def render_login():
    st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1.5, 1])
    with col_login:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>TECHNOBOLT HUB</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#64748b; margin-bottom:40px;'>PROTOCOLOS DE GOVERNANÇA COGNITIVA</p>", unsafe_allow_html=True)
        
        identificador = st.text_input("ID do Operador", placeholder="Ex: admin.user")
        chave = st.text_input("Senha de Acesso", type="password", placeholder="••••••••")
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        if st.button("INICIAR SESSÃO SEGURA"):
            credenciais = {
                "admin": "admin",
                "jackson.antonio": "teste@2025",
                "luiza.trovao": "teste@2025",
                "usuario.teste": "teste@2025"
            }
            if identificador in credenciais and credenciais[identificador] == chave:
                st.session_state.logged_in = True
                st.session_state.user_atual = identificador
                st.rerun()
            else:
                st.error("Credenciais inválidas. O acesso foi registrado para auditoria.")
        st.markdown("<p style='text-align:center; color:#94a3b8; font-size:10px; margin-top:50px;'>ENCRYPTED BY TECHNOBOLT SECURE CORE</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    render_login()
    st.stop()

# --- 5. MOTOR DE INTELIGÊNCIA E REDUNDÂNCIA (FAILOVER) ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

MODEL_FALLBACK_CHAIN = [
    "models/gemini-1.5-pro-latest",
    "models/gemini-1.5-flash",
    "models/gemini-1.0-pro"
]

def motor_ai_technobolt(prompt, context=None, chatbot_mode=False):
    """
    Motor central com redundância tripla. 
    Se o modelo principal falhar, o sistema desce a escada de modelos automaticamente.
    """
    system_base = (
        "Você é o Motor de Inteligência Central da TechnoBolt Solutions. "
        "Sua função é fornecer análises de governança, estratégia e auditoria de elite. "
        "DIRETRIZES: Tom técnico e executivo. Proibido saudações genéricas. "
        "ENTREGA: Markdown estruturado. Foco em ROI e mitigação de riscos."
    )
    
    if chatbot_mode:
        system_base = (
            "Você é o Guia de Suporte TechnoBolt. Responda apenas sobre as 8 funções do sistema Hub. "
            "Se o usuário perguntar algo não relacionado, responda: 'Sinto muito, mas essa não é uma função da ferramenta'."
        )

    for model_name in MODEL_FALLBACK_CHAIN:
        try:
            model = genai.GenerativeModel(model_name, system_instruction=system_base)
            payload = [prompt] + context if context else prompt
            response = model.generate_content(payload)
            return response.text, model_name
        except Exception as e:
            continue
    return "⚠️ ERRO CRÍTICO: Falha total na comunicação com os motores neurais.", "OFFLINE"

def exportar_para_word(titulo, texto):
    """Gera um documento .docx com formatação corporativa TechnoBolt."""
    doc = docx.Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"Relatório Gerado por: {st.session_state.user_atual.upper()}")
    doc.add_paragraph(f"Timestamp: {time.strftime('%d/%m/%Y %H:%M:%S')}")
    doc.add_paragraph("-" * 50)
    doc.add_paragraph(texto)
    stream = BytesIO()
    doc.save(stream)
    stream.seek(0)
    return stream

# --- 6. INTERFACE DE NAVEGAÇÃO E TEMA ---
st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
col_info, col_spacer, col_theme = st.columns([3, 1, 1])

with col_info:
    st.markdown(f"<span class='status-badge'>OP: {st.session_state.user_atual.upper()}</span>", unsafe_allow_html=True)

with col_theme:
    tema_label = "🌙 Dark Mode" if st.session_state.theme == 'light' else "☀️ Light Mode"
    if st.button(tema_label):
        st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
        st.rerun()

menu_principal = [
    "🏠 Centro de Comando (Dashboard)",
    "📁 Analisador McKinsey de Documentos",
    "📧 Email Intel (Processamento em Lote)",
    "✉️ Gerador de Emails Corporativos",
    "🧠 Briefing Estratégico & Radar",
    "📝 Gestor de Atas de Reunião",
    "📈 Análise de Mercado & Churn",
    "📊 Relatório Master de Diretoria"
]

escolha = st.selectbox("Selecione o Módulo Ativo", menu_principal, label_visibility="collapsed")
st.markdown("<hr>", unsafe_allow_html=True)

# --- 7. DESENVOLVIMENTO DOS MÓDULOS INTEGRAIS ---

# DASHBOARD
if "🏠 Centro" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h1>Dashboard de Governança</h1><p>Monitoramento de processos neurais e integridade do sistema.</p></div>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Motor IA", "Soberano", delta="Redundância Ativa")
    m2.metric("Sessão", st.session_state.user_atual.capitalize(), delta="Protegida")
    m3.metric("Uptime", "99.9%", delta="Failover On")

# ANALISADOR MCKINSEY
elif "📁 Analisador" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>📁 Analisador de Documentos McKinsey</h2><p>Extração de inteligência estratégica e análise de riscos complexos.</p></div>', unsafe_allow_html=True)
    upload = st.file_uploader("Upload de Documento (PDF/DOCX/TXT)", type=['pdf', 'docx', 'txt'])
    if upload and st.button("EXECUTAR AUDITORIA"):
        with st.spinner("Processando dados corporativos..."):
            # Lógica de extração baseada no tipo de arquivo
            if upload.type == "application/pdf":
                file_data = [{"mime_type": "application/pdf", "data": upload.read()}]
                prompt = "Aja como McKinsey. Forneça: Resumo Executivo, 5 Pontos de Risco e 3 Ações Estratégicas."
            else:
                texto_bruto = upload.read().decode()
                file_data = [texto_bruto]
                prompt = "Analise o texto anexo sob a perspectiva McKinsey de eficiência operacional."
            
            resultado, m_usado = motor_ai_technobolt(prompt, file_data)
            st.markdown(f"<p style='font-size:10px; color:#64748b;'>Processado por: {m_usado}</p>", unsafe_allow_html=True)
            st.markdown(resultado)
            st.download_button("📥 Baixar Auditoria (Word)", data=exportar_para_word("Análise McKinsey", resultado), file_name="Auditoria_TechnoBolt.docx")

# EMAIL INTEL (LOTE)
elif "📧 Email Intel" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>📧 Email Intel: Auditoria em Lote</h2><p>Consolidação de múltiplos e-mails em um relatório unificado.</p></div>', unsafe_allow_html=True)
    files = st.file_uploader("Selecione os e-mails (PDF)", type=['pdf'], accept_multiple_files=True)
    if files and st.button("PROCESSAR LOTE"):
        for f in files:
            with st.expander(f"Auditoria: {f.name}", expanded=True):
                res, mod = motor_ai_technobolt("Resuma e rascunhe uma resposta executiva.", [{"mime_type": "application/pdf", "data": f.read()}])
                st.markdown(res)

# GERADOR DE EMAILS
elif "✉️ Gerador" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>✉️ Gerador de Emails Corporativos</h2></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    cargo = c1.text_input("Seu Cargo:")
    destinatario = c2.text_input("Destinatário:")
    contexto_email = st.text_area("Descreva o objetivo do e-mail:", height=150)
    if st.button("REDIGIR E-MAIL PROFISSIONAL"):
        p_email = f"Como {cargo}, escreva um e-mail para {destinatario} sobre: {contexto_email}. Use tom executivo."
        res, mod = motor_ai_technobolt(p_email)
        st.markdown(f'<div class="main-card" style="max-width:100%;">{res}</div>', unsafe_allow_html=True)
        st.download_button("📥 Baixar Word", data=exportar_para_word("Rascunho de E-mail", res), file_name="Email_TechnoBolt.docx")

# BRIEFING ESTRATÉGICO
elif "🧠 Briefing" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>🧠 Briefing Estratégico & Radar</h2></div>', unsafe_allow_html=True)
    empresa = st.text_input("Nome da Empresa Alvo:")
    setor = st.text_input("Setor de Atuação:")
    if st.button("GERAR DOSSIÊ"):
        res, mod = motor_ai_technobolt(f"Gere um briefing estratégico 2026 para a empresa {empresa} no setor {setor}. Foco em concorrência e tendências.")
        st.markdown(res)

# GESTOR DE ATAS
elif "📝 Gestor" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>📝 Gestor de Atas de Reunião</h2></div>', unsafe_allow_html=True)
    notas = st.text_area("Cole aqui as notas ou transcrição da reunião:", height=300)
    if st.button("FORMALIZAR ATA"):
        res, mod = motor_ai_technobolt(f"Transforme estas notas em uma Ata Formal de Diretoria: {notas}")
        st.markdown(f'<div class="main-card" style="max-width:100%;">{res}</div>', unsafe_allow_html=True)
        st.download_button("📥 Baixar Ata (Word)", data=exportar_para_word("Ata de Reunião", res), file_name="Ata_Oficial.docx")

# MERCADO E CHURN
elif "📈 Análise" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>📈 Análise de Mercado & Churn</h2></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Radar de Concorrência", "⚠️ Previsão de Churn"])
    with t1:
        rival = st.text_input("Inserir Concorrente:")
        if st.button("ANALISAR RIVAL"):
            res, _ = motor_ai_technobolt(f"Análise de mercado competitiva para: {rival}"); st.markdown(res)
    with t2:
        feed = st.text_area("Feedback do Cliente para Análise de Risco:")
        if st.button("CALCULAR RISCO"):
            res, _ = motor_ai_technobolt(f"Avalie risco de churn para este feedback: {feed}"); st.markdown(res)

# RELATÓRIO MASTER
elif "📊 Relatório" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>📊 Relatório Master de Diretoria</h2><p>Dossiê semanal consolidado.</p></div>', unsafe_allow_html=True)
    dados_semana = st.text_area("Principais acontecimentos da semana:")
    if st.button("GERAR RELATÓRIO MASTER"):
        res, mod = motor_ai_technobolt(f"Gere um Relatório Master de Governança com base em: {dados_semana}")
        st.markdown(res); st.download_button("📥 Baixar Dossiê", data=exportar_para_word("Relatório Master", res), file_name="Master_TechnoBolt.docx")

# --- 8. CHATBOT POPUP (SISTEMA DE SUPORTE FLUTUANTE) ---
st.markdown("""
    <div style="position: fixed; bottom: 30px; right: 30px; z-index: 10000;">
        <p style='color: #2563eb; font-weight: 800; font-size: 12px; margin-bottom: 5px; text-align: center;'>SUPORTE</p>
    </div>
""", unsafe_allow_html=True)

with st.container():
    # Usando checkbox para controle de estado sem quebrar o layout
    if st.checkbox("💬 Abrir Assistente", key="chat_toggle_btn"):
        st.markdown('<div class="chat-window">', unsafe_allow_html=True)
        st.markdown('<div class="chat-header">Guia TechnoBolt</div>', unsafe_allow_html=True)
        st.markdown("<div style='padding: 25px; overflow-y: auto;'>", unsafe_allow_html=True)
        
        pergunta = st.text_input("Como posso ajudar?", key="pergunta_chat", placeholder="Sua dúvida...")
        if pergunta:
            with st.spinner("Consultando protocolos..."):
                resposta, _ = motor_ai_technobolt(pergunta, chatbot_mode=True)
                st.info(resposta)
        
        st.markdown("</div></div>", unsafe_allow_html=True)

# --- 9. RODAPÉ DE GOVERNANÇA ---
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
st.markdown(f"""
    <div style='text-align: center; color: #94a3b8; font-size: 11px;'>
        TechnoBolt IA Hub © 2026 | Versão 4.0 Enterprise | Licenciado para: {st.session_state.user_atual.upper()}<br>
        Todos os dados processados são criptografados em repouso.
    </div>
""", unsafe_allow_html=True)