import streamlit as st
import google.generativeai as genai
import os
import time
import docx  # Requer: pip install python-docx
from io import BytesIO
import base64
import signal
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# --- 1. CONFIGURAÇÃO DE SEGURANÇA E PROTOCOLO (ELITE HUB) ---
st.set_page_config(
    page_title="TechnoBolt IA - Elite Hub de Governança",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. GESTÃO DE ESTADO (INICIALIZAÇÃO BLINDADA) ---
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
    'last_update': time.time(),
    'login_time': time.time(),
    'uso_sessao': {},
    'mostrar_resultado': False,
    'resultado_ia': "",
    'titulo_resultado': ""
}

for chave, valor in chaves_sessao.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor

# --- LÓGICA DE NOTIFICAÇÃO ---
def enviar_notificacao_email(assunto, corpo):
    sg_key = os.environ.get("SENDGRID_API_KEY") 
    message = Mail(
        from_email='technoboltconsultoria@gmail.com',
        to_emails='technoboltconsultoria@gmail.com',
        subject=assunto,
        plain_text_content=corpo)
    try:
        sg = SendGridAPIClient(sg_key)
        sg.send(message)
        return True
    except: return False

def protocol_logout():
    st.session_state.logged_in = False
    st.session_state.user_atual = None
    st.rerun()

def registrar_evento(funcao):
    if 'uso_sessao' not in st.session_state: st.session_state.uso_sessao = {}
    st.session_state.uso_sessao[funcao] = st.session_state.uso_sessao.get(funcao, 0) + 1

# --- 3. DESIGN SYSTEM (PREMIUM DARK EXCLUSIVE - ADJUSTED BARS & FORMS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* RESET GLOBAL PARA BRANCO */
    html, body, [data-testid="stAppViewContainer"], .stApp, p, h1, h2, h3, h4, span, label, div { 
        color: #ffffff !important; 
        font-family: 'Inter', sans-serif !important; 
    }
    
    html, body, [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    [data-testid="stHeader"], [data-testid="stSidebar"] { display: none !important; }

    /* CARDS E FORMS ESCUROS */
    .main-card { 
        background: linear-gradient(145deg, #0d0d0d, #1a1a1a); 
        border: 1px solid #333; 
        border-radius: 20px; 
        padding: 40px; 
        margin-bottom: 25px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.8); 
    }

    /* AJUSTE DO FUNDO DOS FORMS */
    [data-testid="stForm"] {
        background-color: #0d0d0d !important;
        border: 1px solid #333 !important;
        border-radius: 20px !important;
        padding: 20px !important;
    }

    /* ESTILIZAÇÃO DE INPUTS, TEXTAREAS E SELECTS (BARRA DE TAREFAS/LISTA SUSPENSA) */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
    }

    /* REMOVER BRANCO DA LISTA SUSPENSA (OPTIONS) */
    div[data-baseweb="popover"] > div, ul[role="listbox"] {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333 !important;
    }
    
    li[role="option"] {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }
    
    li[role="option"]:hover {
        background-color: #3b82f6 !important;
    }
    
    /* GARANTIR QUE O TEXTO DENTRO DOS INPUTS SEJA BRANCO */
    input, textarea, select {
        color: #ffffff !important;
    }

    .hero-title { 
        font-size: 38px; 
        font-weight: 800; 
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        letter-spacing: -1px; 
        text-align: center; 
    }

    .stButton > button { 
        width: 100%; 
        border-radius: 12px; 
        height: 3.5em; 
        font-weight: 700; 
        background: #3b82f6 !important; 
        color: white !important; 
        border: none !important; 
        transition: 0.3s; 
    }

    .stButton > button:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3) !important; 
    }

    .result-card-unificado { 
        background: #080808; 
        border-left: 4px solid #3b82f6; 
        border-radius: 12px; 
        padding: 30px; 
        border: 1px solid #1a1a1a; 
        line-height: 1.7; 
    }

    .status-badge { 
        padding: 4px 12px; 
        border-radius: 50px; 
        background: #111; 
        color: #3b82f6 !important; 
        font-size: 11px; 
        font-weight: 700; 
        border: 1px solid #333; 
    }

    .stMetric { 
        background: #0d0d0d !important; 
        border: 1px solid #222 !important; 
        border-radius: 15px !important; 
        padding: 15px !important; 
    }
    
    /* FORÇAR LABEL DAS MÉTRICAS */
    [data-testid="stMetricLabel"] p {
        color: #888888 !important;
    }
    [data-testid="stMetricValue"] div {
        color: #ffffff !important;
    }

    header, footer { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. MOTOR DE INTELIGÊNCIA ESPECIALIZADA COM RODÍZIO DE CHAVES ---
MODEL_FAILOVER_LIST = ["models/gemini-3-flash-preview", "models/gemini-2.5-flash", "models/gemini-2.0-flash", "models/gemini-flash-latest"]

def call_technobolt_ai(prompt, attachments=None, system_context="default"):
    chaves = [os.environ.get(f"GEMINI_CHAVE_{i}") for i in range(1, 8)]
    chaves = [k for k in chaves if k]
    if not chaves:
        chave_unica = os.environ.get("GEMINI_API_KEY")
        if chave_unica: chaves = [chave_unica]

    p = st.session_state.perfil_cliente
    dna_context = f"DNA TECHNOBOLT: Empresa {p['nome_empresa']} do setor {p['setor']}. Missão: {p['missao']}. Tom: {p['tom_voz']}.\n"
    
    contexts = {
        "mckinsey": (
            "Você é um Sócio Sênior da McKinsey & Company. Sua tarefa é realizar uma auditoria estratégica MECE. "
            "Aplique o framework McKinsey 7S. Identifique lacunas de ROI e riscos operacionais. "
            "Formate a resposta com: 1. Resumo Executivo, 2. Diagnóstico de Gargalos, 3. Matriz de Priorização, 4. Pontos de Atenção, 5. Plano de Ação."
        ),
        "email_intel": (
            "Você é o Chief Communications Officer (CCO). Analise este lote de e-mails para triagem executiva. "
            "Identifique urgências, oportunidades de negócio e rascunhe respostas diplomáticas de alto nível."
        ),
        "briefing": (
            "Você é o Diretor de Inteligência Competitiva. Realize um Scan PESTEL e Forças de Porter. "
            "Seu objetivo é antecipar movimentos de mercado e ameaças de novos entrantes."
        ),
        "ata": (
            "Você é um Secretário de Governança com experiência em conselhos listados na B3. "
            "Formalize os pontos em Ata de Diretoria. Use a Matriz RACI para definir responsabilidades claras."
        ),
        "churn": (
            "Você é um Especialista em Customer Success e Ciência de Dados. "
            "Analise os indicadores de comportamento e feedbacks para prever risco de perda de cliente (Churn) e sugira planos de retenção."
        ),
        "master": (
            "Você é o Chief Operating Officer (COO). Consolide os KPIs e eventos da semana em um dossiê de diretoria. "
            "Foque em produtividade, eficiência de recursos e próximos marcos (milestones)."
        ),
        "default": "Você é o Motor de Inteligência TechnoBolt. Postura de consultoria sênior, direto e analítico."
    }
    
    final_sys_instr = dna_context + contexts.get(system_context, contexts["default"])
    
    for idx, key in enumerate(chaves):
        try:
            genai.configure(api_key=key)
            for model_name in MODEL_FAILOVER_LIST:
                try:
                    model = genai.GenerativeModel(model_name, system_instruction=final_sys_instr)
                    payload = [prompt] + attachments if attachments else prompt
                    response = model.generate_content(payload)
                    return response.text, f"CHAVE {idx+1} - {model_name}"
                except: continue
        except: continue

    return "⚠️ Todos os motores e chaves estão offline ou com limite excedido.", "OFFLINE"

# --- 5. TELA DE LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1.2, 1])
    with col_login:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>TECHNOBOLT HUB</h1>", unsafe_allow_html=True)
        user_id = st.text_input("Operador", placeholder="Usuário")
        user_key = st.text_input("Chave", type="password", placeholder="Senha")
        if st.button("CONECTAR"):
            banco_users = {"admin": "admin","anderson.bezerra": "teste@2025", "fabricio.felix": "teste@2025", "jackson.antonio": "teste@2025", "luiza.trovao": "teste@2025"}
            if user_id in banco_users and banco_users[user_id] == user_key:
                st.session_state.logged_in = True
                st.session_state.user_atual = user_id
                st.rerun()
    st.stop()

# --- 6. INTERFACE PRINCIPAL ---
st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
head_l, head_r = st.columns([4, 1])
with head_l:
    st.markdown(f"**OPERADOR:** <span class='status-badge'>{st.session_state.user_atual.upper()}</span>", unsafe_allow_html=True)
with head_r:
    if st.button("🚪 Sair"): protocol_logout()

menu_navegacao = [
    "🏠 Centro de Comando", 
    "📁 Analisador de Documentos", 
    "📧  Analisador de E-mails", 
    "✉️ Gerador de Emails", 
    "🧠 Briefing Estratégico", 
    "📝 Gerador de Atas", 
    "📈 Mercado & Churn", 
    "📊 Relatório Semanal"
]
escolha = st.selectbox("Seletor de Módulo", menu_navegacao, label_visibility="collapsed")
st.markdown("<hr style='margin: 10px 0 35px 0; border: 0.5px solid #222;'>", unsafe_allow_html=True)

# --- 7. LÓGICA DOS MÓDULOS ---

if "🏠 Centro" in escolha:
    st.markdown("""<div class="main-card" style="text-align:center;">
        <h2 style='color:#3b82f6;'>Soberania Digital TechnoBolt</h2>
        <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXlsaTYwaDZkeGc2MjMxcXk4MWJjMGtwcHEwNTZ6dHFkaXV0NzNxbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eljCVpMrhepUSgZaVP/giphy.gif" width="350">
    </div>""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Status IA", "Soberana")
    c2.metric("Sessão", st.session_state.user_atual.capitalize())
    c3.metric("DNA Ativo", st.session_state.perfil_cliente["nome_empresa"])

elif "📁 Analisador de Documentos" in escolha:
    st.markdown('<div class="main-card"><h2>📁 Analisador de Documentos</h2><p>Auditoria estratégica de documentos.</p></div>', unsafe_allow_html=True)
    up = st.file_uploader("Submeter PDF ou DOCX:", type=['pdf', 'docx'])
    if up and st.button("EXECUTAR ANÁLISE"):
        registrar_evento("Analisador")
        with st.spinner("Executando Protocolo Technobolt..."):
            dados = [{"mime_type": "application/pdf", "data": up.read()}] if up.type == "application/pdf" else [up.read().decode(errors='ignore')]
            res, motor = call_technobolt_ai("Audite este documento.", dados, "mckinsey")
            st.session_state.titulo_resultado = f"Relatório Revisado ({motor})"
            st.session_state.resultado_ia = res
            st.session_state.mostrar_resultado = True
            st.rerun()

elif "📧 Analisador de E-mails" in escolha:
    st.markdown('<div class="main-card"><h2>📧  Analisador de E-mails</h2><p>Triagem e rascunhos de alta performance.</p></div>', unsafe_allow_html=True)
    txt_emails = st.text_area("Cole aqui o conteúdo dos e-mails (um por linha ou bloco):", height=200)
    if st.button("PROCESSAR"):
        registrar_evento("Email Intel")
        with st.spinner("CCO analisando comunicações..."):
            res, motor = call_technobolt_ai(txt_emails, None, "email_intel")
            st.session_state.titulo_resultado = f"Resultado da análise: ({motor})"
            st.session_state.resultado_ia = res
            st.session_state.mostrar_resultado = True
            st.rerun()

elif "✉️ Gerador" in escolha:
    st.markdown('<div class="main-card"><h2>✉️ Gerador de Emails de Elite</h2></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    cargo = c1.text_input("Seu Cargo:")
    pauta = st.text_area("Assunto/Pauta:")
    if st.button("GERAR EMAIL"):
        registrar_evento("Gerador")
        res, motor = call_technobolt_ai(f"De: {cargo}. Pauta: {pauta}", None, "email")
        st.session_state.titulo_resultado = f"Email Gerado ({motor})"
        st.session_state.resultado_ia = res
        st.session_state.mostrar_resultado = True
        st.rerun()

elif "🧠 Briefing" in escolha:
    st.markdown('<div class="main-card"><h2>🧠 Briefing Estratégico</h2><p>Radar de mercado e análise competitiva.</p></div>', unsafe_allow_html=True)
    target = st.text_input("Empresa ou Setor Alvo:")
    if st.button("EXECUTAR SCAN DE MERCADO"):
        registrar_evento("Briefing")
        with st.spinner("Coletando inteligência competitiva..."):
            res, motor = call_technobolt_ai(f"Analise o setor/empresa: {target}", None, "briefing")
            st.session_state.titulo_resultado = f"Dossiê: {target} ({motor})"
            st.session_state.resultado_ia = res
            st.session_state.mostrar_resultado = True
            st.rerun()

elif "📝 Gerador de Atas" in escolha:
    st.markdown('<div class="main-card"><h2>📝 Gestor de Atas de Governança</h2></div>', unsafe_allow_html=True)
    notas = st.text_area("Notas da Reunião:", height=200)
    if st.button("FORMALIZAR ATA"):
        registrar_evento("Atas")
        res, motor = call_technobolt_ai(notas, None, "ata")
        st.session_state.titulo_resultado = f"Ata de Reunião Oficial ({motor})"
        st.session_state.resultado_ia = res
        st.session_state.mostrar_resultado = True
        st.rerun()

elif "📈 Mercado & Churn" in escolha:
    st.markdown('<div class="main-card"><h2>📈 Inteligência de Mercado & Churn</h2><p>Previsão de perda e análise de retenção.</p></div>', unsafe_allow_html=True)
    data_churn = st.text_area("Feedbacks ou métricas do cliente:")
    if st.button("CALCULAR RISCO"):
        registrar_evento("Churn")
        with st.spinner("Avaliando probabilidade de evasão..."):
            res, motor = call_technobolt_ai(data_churn, None, "churn")
            st.session_state.titulo_resultado = f"Diagnóstico de Retenção ({motor})"
            st.session_state.resultado_ia = res
            st.session_state.mostrar_resultado = True
            st.rerun()

elif "📊 Relatório Semanal" in escolha:
    st.markdown('<div class="main-card"><h2>📊 Relatório Semanal</h2><p>Consolidação de KPIs e eventos semanais.</p></div>', unsafe_allow_html=True)
    kpis = st.text_area("Fatos e métricas da semana:")
    if st.button("GERAR RELATÓRIO SEMANAL"):
        registrar_evento("Relatório Master")
        with st.spinner("COO consolidando dados..."):
            res, motor = call_technobolt_ai(kpis, None, "master")
            st.session_state.titulo_resultado = f"Relatório Semanal ({motor})"
            st.session_state.resultado_ia = res
            st.session_state.mostrar_resultado = True
            st.rerun()

# --- 8. COMPONENTE DE RESULTADO UX ---
if st.session_state.get('mostrar_resultado'):
    st.markdown("---")
    _, col_res, _ = st.columns([1, 8, 1])
    with col_res:
        st.markdown(f"<div class='result-card-unificado'><h2 style='color:#3b82f6;'>{st.session_state.titulo_resultado}</h2>", unsafe_allow_html=True)
        st.markdown(st.session_state.resultado_ia)
        st.markdown("</div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([2, 2, 2])
        if c1.button("📥 Baixar Relatório"):
            doc = docx.Document()
            doc.add_heading(st.session_state.titulo_resultado, 0)
            doc.add_paragraph(st.session_state.resultado_ia)
            buf = BytesIO(); doc.save(buf); buf.seek(0)
            st.download_button("Clique para Download", buf, "technobolt_relatorio.docx")
        if c3.button("✖️ Fechar"):
            st.session_state.mostrar_resultado = False
            st.rerun()

# --- 9. RODAPÉ ---
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
st.caption(f"TechnoBolt Solutions © 2026 | Operador: {st.session_state.user_atual.upper()} | HUB Elite")
