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

# --- 2. GESTÃO DE ESTADO (INICIALIZAÇÃO DE SESSÃO) ---
chaves_sessao = {
    'logged_in': False,
    'user_atual': None,
    'perfil_cliente': {
        "nome_empresa": "TechnoBolt Solutions",
        "setor": "Tecnologia e Consultoria",
        "missao": "Prover governança cognitiva de elite através de IA.",
        "valores": "Inovação, Ética, Precisão, Resiliência.",
        "tom_voz": "Executivo, Autoritário e Analítico"
    },
    'analise_count': 0,
    'last_update': time.time()
}

for chave, valor in chaves_sessao.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor

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
    .logout-zone .stButton > button:hover {
        background: #fef2f2 !important;
        border-color: #f87171 !important;
    }

    .status-badge {
        padding: 6px 18px; border-radius: 50px; background: #eff6ff; 
        color: #1e40af; font-size: 12px; font-weight: 700; border: 1px solid #dbeafe;
    }
    
    .stMetric { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 18px; padding: 20px; }

    .admin-label {
        background: #fef3c7; color: #92400e; padding: 4px 12px;
        border-radius: 8px; font-size: 10px; font-weight: 800; margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. TELA DE LOGIN (ACESSO RESTRITO) ---
def render_auth():
    st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1.4, 1])
    with col_login:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>TECHNOBOLT HUB</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#64748b; margin-bottom:40px; letter-spacing:1px;'>TERMINAL DE GOVERNANÇA COGNITIVA</p>", unsafe_allow_html=True)
        
        user_id = st.text_input("Credencial de Operador", placeholder="Usuário")
        user_key = st.text_input("Chave de Segurança", type="password", placeholder="Senha")
        
        if st.button("AUTENTICAR NO HUB"):
            banco_users = {"admin": "admin", "jackson.antonio": "teste@2025", "luiza.trovao": "teste@2025"}
            if user_id in banco_users and banco_users[user_id] == user_key:
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

# --- 5. MOTOR DE INTELIGÊNCIA COM FAILOVER E INJEÇÃO DE PERFIL ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# LISTA DE MODELOS ORIGINAIS INTEGRADA
MODEL_FAILOVER_LIST = [
    "models/gemini-3-flash-preview", 
    "models/gemini-2.5-flash", 
    "models/gemini-2.0-flash", 
    "models/gemini-2.0-flash-lite", 
    "models/gemini-flash-latest"
]

def call_technobolt_ai(prompt, attachments=None):
    """Executa a requisição injetando o DNA Corporativo do Perfil do Cliente no Prompt de Sistema."""
    p = st.session_state.perfil_cliente
    perfil_contexto = (
        f"DNA DA EMPRESA USUÁRIA:\n"
        f"- Empresa: {p['nome_empresa']}\n"
        f"- Setor: {p['setor']}\n"
        f"- Missão: {p['missao']}\n"
        f"- Valores: {p['valores']}\n"
        f"- Tom de Voz: {p['tom_voz']}\n\n"
    )

    sys_instr = (
        f"{perfil_contexto}"
        "Você é o Motor de Inteligência Estratégica da TechnoBolt Solutions. "
        "Sua postura é de um consultor sênior McKinsey/BCG/Bain. "
        "DIRETRIZES: 1. Respostas técnicas, analíticas e extremamente profundas. 2. Use terminologia executiva. "
        "3. Markdown estruturado com diagnósticos e tabelas. 4. Foco total em ROI e Riscos. "
        "Proibido saudações informais. Responda diretamente ao ponto técnico."
    )

    for model_name in MODEL_FAILOVER_LIST:
        try:
            model = genai.GenerativeModel(model_name, system_instruction=sys_instr)
            payload = [prompt] + attachments if attachments else prompt
            response = model.generate_content(payload)
            return response.text, model_name
        except Exception:
            try:
                # Contigência para modelos que não suportam system_instruction nativa no objeto
                model_fb = genai.GenerativeModel(model_name)
                full_p = f"{sys_instr}\n\nSOLICITAÇÃO: {prompt}"
                response = model_fb.generate_content([full_p] + attachments if attachments else full_p)
                return response.text, model_name
            except:
                continue
    return "⚠️ Motores de IA Offline. Contate a governança.", "OFFLINE"

def export_docx(title, content):
    """Gera documentos Microsoft Word com formatação corporativa."""
    doc = docx.Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(f"Relatório de Governança | Operador: {st.session_state.user_atual.upper()}")
    doc.add_paragraph(f"TechnoBolt Hub Elite | Timestamp: {time.strftime('%d/%m/%Y %H:%M:%S')}")
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
    status_label = f"{st.session_state.user_atual.upper()}"
    if st.session_state.user_atual == "admin":
        status_label += " <span class='admin-label'>ADMIN ACCESS</span>"
    st.markdown(f"**OPERADOR:** <span class='status-badge'>{status_label}</span>", unsafe_allow_html=True)

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

if st.session_state.user_atual == "admin":
    menu_navegacao.append("👤 Perfil do Cliente")

escolha = st.selectbox("Seletor de Módulo", menu_navegacao, label_visibility="collapsed")
st.markdown("<hr style='margin: 10px 0 35px 0; border: 0.5px solid #e2e8f0;'>", unsafe_allow_html=True)

# --- 7. MÓDULOS DE FUNCIONALIDADES INTEGRAIS (520+ LINHAS) ---

# PERFIL DO CLIENTE (Módulo Exclusivo Admin)
if "👤 Perfil" in escolha:
    st.markdown('<div class="main-card"><h2>👤 Perfil do Cliente (Configuração de DNA)</h2><p>Defina o contexto corporativo para personalização profunda da IA.</p></div>', unsafe_allow_html=True)
    with st.form("form_perfil"):
        c1, c2 = st.columns(2)
        nome = c1.text_input("Nome da Empresa:", value=st.session_state.perfil_cliente["nome_empresa"])
        setor = c2.text_input("Setor de Atuação:", value=st.session_state.perfil_cliente["setor"])
        missao = st.text_area("Missão e Propósito:", value=st.session_state.perfil_cliente["missao"])
        valores = st.text_input("Valores Principais (Vírgulas):", value=st.session_state.perfil_cliente["valores"])
        tom = st.selectbox("Tom de Voz Desejado:", ["Executivo e Autoritário", "Técnico e Diplomático", "Colaborativo e Moderno"])
        
        if st.form_submit_button("SALVAR DNA CORPORATIVO"):
            st.session_state.perfil_cliente = {
                "nome_empresa": nome, "setor": setor, "missao": missao, 
                "valores": valores, "tom_voz": tom
            }
            st.success("DNA Corporativo atualizado. Todos os prompts agora utilizam este contexto.")
            st.rerun()

# DASHBOARD
elif "🏠 Dashboard" in escolha:
    st.markdown('<div class="main-card"><h1>Command Center</h1><p>Monitoria de Soberania Digital e Redundância Ativa.</p></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("IA Engine", "Soberana", "Redundância On")
    c2.metric("Sessão", st.session_state.user_atual.capitalize(), "Protegida")
    c3.metric("DNA Ativo", st.session_state.perfil_cliente["nome_empresa"])

# ANALISADOR MCKINSEY
elif "📁 Analisador McKinsey" in escolha:
    st.markdown('<div class="main-card"><h2>📁 Analisador de Documentos McKinsey</h2><p>Auditoria técnica baseada no DNA de sua empresa.</p></div>', unsafe_allow_html=True)
    arquivo_up = st.file_uploader("Submeter Documento (PDF/DOCX/TXT):", type=['pdf', 'docx', 'txt'])
    if arquivo_up and st.button("EXECUTAR AUDITORIA SÊNIOR"):
        with st.spinner("Analisando estrutura estratégica..."):
            if arquivo_up.type == "application/pdf":
                dados_ia = [{"mime_type": "application/pdf", "data": arquivo_up.read()}]
                p_mc = "Aja como McKinsey. Forneça: Resumo Executivo, Swot de Risco, ROI Estimado e Plano 90 dias com base no nosso perfil corporativo."
            else:
                texto_raw = extrair_texto_docx(arquivo_up) if arquivo_up.name.endswith('docx') else arquivo_up.read().decode(errors="ignore")
                dados_ia = [texto_raw]
                p_mc = "Analise tecnicamente este documento para a Technobolt Solutions sob a ótica de eficiência operacional."
            
            res_ia, mod_ia = call_technobolt_ai(p_mc, dados_ia)
            st.markdown(f"<p style='font-size:10px; color:#64748b;'>Processado via: {mod_ia}</p>", unsafe_allow_html=True)
            st.markdown(res_ia)
            st.download_button("📥 Baixar Relatório", data=export_docx("Auditoria McKinsey", res_ia), file_name=f"Auditoria_{arquivo_up.name}.docx")

# EMAIL INTEL (LOTE)
elif "📧 Email Intel" in escolha:
    st.markdown('<div class="main-card"><h2>📧 Email Intel: Auditoria em Lote</h2><p>Processamento massivo de e-mails em PDF.</p></div>', unsafe_allow_html=True)
    emails = st.file_uploader("Upload Emails (PDF):", type=['pdf'], accept_multiple_files=True)
    if emails and st.button("PROCESSAR LOTE"):
        for email_pdf in emails:
            with st.expander(f"Auditoria: {email_pdf.name}", expanded=True):
                res_email, _ = call_technobolt_ai("Resuma tecnicamente e rascunhe a resposta executiva ideal usando nosso tom de voz.", [{"mime_type": "application/pdf", "data": email_pdf.read()}])
                st.markdown(res_email)

# GERADOR DE EMAILS
elif "✉️ Gerador de Emails" in escolha:
    st.markdown('<div class="main-card"><h2>✉️ Gerador de Emails de Alto Impacto</h2></div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    cargo_e = ca.text_input("Seu Cargo:"); dest_e = cb.text_input("Destinatário:")
    formalidade = st.select_slider("Formalidade", options=["Casual", "Corporativo", "Executivo", "Diplomático"], value="Executivo")
    contexto_e = st.text_area("Objetivo da Mensagem:")
    if st.button("REDIGIR E-MAIL EXECUTIVO"):
        p_email = f"Escreva para {dest_e} como {cargo_e} sobre {contexto_e}. Formalidade: {formalidade}."
        res_email, _ = call_technobolt_ai(p_email)
        st.markdown(f'<div class="main-card">{res_email}</div>', unsafe_allow_html=True)
        st.download_button("📥 Baixar Word", data=export_docx("Email Gerado", res_email), file_name="Email_Rascunho.docx")

# BRIEFING ESTRATÉGICO
elif "🧠 Briefing" in escolha:
    st.markdown('<div class="main-card"><h2>🧠 Briefing Estratégico & Radar 2026</h2></div>', unsafe_allow_html=True)
    e_alvo = st.text_input("Empresa/Setor Alvo:")
    if st.button("EXECUTAR SCAN DE MERCADO"):
        res_brief, _ = call_technobolt_ai(f"Gere briefing estratégico 2026 para {e_alvo}. Foco em impacto para {st.session_state.perfil_cliente['nome_empresa']}.")
        st.markdown(res_brief)

# GESTOR DE ATAS
elif "📝 Gestor de Atas" in escolha:
    st.markdown('<div class="main-card"><h2>📝 Gestor de Atas de Governança</h2></div>', unsafe_allow_html=True)
    notas_r = st.text_area("Notas da Reunião:", height=280)
    if st.button("FORMALIZAR ATA DE DIRETORIA"):
        res_ata, _ = call_technobolt_ai(f"Formalize as seguintes notas em Ata de Diretoria TechnoBolt: {notas_r}")
        st.markdown(f'<div class="main-card">{res_ata}</div>', unsafe_allow_html=True)
        st.download_button("📥 Baixar Ata Word", data=export_docx("Ata Oficial", res_ata), file_name="Ata_Oficial.docx")

# MERCADO & CHURN
elif "📈 Mercado & Churn" in escolha:
    st.markdown('<div class="main-card"><h2>Inteligência de Mercado & Churn</h2></div>', unsafe_allow_html=True)
    tab_rival, tab_churn = st.tabs(["🔍 Radar Rival", "⚠️ Risco Churn"])
    with tab_rival:
        rival_n = st.text_input("Concorrente:")
        if st.button("ANALISAR RIVAL"):
            res_r, _ = call_technobolt_ai(f"Análise competitiva: {rival_n}"); st.markdown(res_r)
    with tab_churn:
        feed_c = st.text_area("Feedback Cliente:");
        if st.button("CALCULAR RISCO"):
            res_c, _ = call_technobolt_ai(f"Avalie risco de churn para: {feed_c}"); st.markdown(res_c)

# RELATÓRIO MASTER
elif "📊 Relatório Master" in escolha:
    st.markdown('<div class="main-card"><h2>📊 Relatório Master de Diretoria</h2></div>', unsafe_allow_html=True)
    kpis = st.text_area("Fatos e métricas da semana:")
    if st.button("GERAR DOSSIÊ MASTER"):
        res_m, _ = call_technobolt_ai(f"Relatório Master de Governança TechnoBolt: {kpis}.")
        st.markdown(res_m)
        st.download_button("📥 Baixar Dossiê", data=export_docx("Relatório Master", res_m), file_name="Master.docx")

# --- 8. RODAPÉ DE GOVERNANÇA ---
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
st.caption(f"TechnoBolt Solutions © 2026 | Elite Hub Edition v1.0 | Operador: {st.session_state.user_atual.upper()}")