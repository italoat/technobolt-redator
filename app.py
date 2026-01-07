import streamlit as st
import smtplib
import google.generativeai as genai
import os
import time
import docx  # Requer: pip install python-docx
from io import BytesIO
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    'last_update': time.time()
}

for chave, valor in chaves_sessao.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor

def protocol_logout():
    """Gera relatório de uso e finaliza a sessão."""
    tempo_logado = round((time.time() - st.session_state.login_time) / 60, 2)
    relatorio_uso = f"""
    Relatório de Uso - Usuário: {st.session_state.user_atual}
    Tempo Total: {tempo_logado} minutos.
    Ações realizadas: {st.session_state.uso_sessao}
    """
    enviar_notificacao_email("Relatório de Uso", relatorio_uso)
    
    st.session_state.logged_in = False
    st.session_state.user_atual = None
    st.rerun()

def enviar_notificacao_email(assunto, corpo):
    """Envia notificações usando SSL na porta 465 (Alta compatibilidade)."""
    remetente = "technoboltconsultoria@gmail.com"
    destinatario = "technoboltconsultoria@gmail.com"
    senha_app = "uxagfbfemjmvawun" 

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        # SMTP_SSL é mais robusto para evitar bloqueios de firewall
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remetente, senha_app)
            server.send_message(msg)
        return True
    except Exception as e:
        # Se falhar, tenta porta 587 como último recurso
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(remetente, senha_app)
                server.send_message(msg)
            return True
        except Exception as e2:
            st.error(f"Falha no envio de e-mail: {e2}")
            return False

def registrar_evento(funcao):
    """Rastreia quais funções o usuário utilizou durante a sessão."""
    if 'uso_sessao' not in st.session_state:
        st.session_state.uso_sessao = {}
    st.session_state.uso_sessao[funcao] = st.session_state.uso_sessao.get(funcao, 0) + 1

def mostrar_popup(titulo, conteudo):
    """Renderiza o popup com suporte a quebra de linha e fechamento via botão."""
    conteudo_html = conteudo.replace('\n', '<br>')
    
    # Criamos um botão do próprio Streamlit para fechar, mudando um estado
    if st.button("✖️ Fechar Visualização"):
        st.rerun()

    st.markdown(f"""
    <div style="
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(15, 23, 42, 0.8); z-index: 9999;
        display: flex; justify-content: center; align-items: center;
        padding: 20px;">
        <div style="
            background: white; padding: 40px; border-radius: 20px;
            max-width: 800px; width: 100%; max-height: 80vh; overflow-y: auto;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            position: relative; border: 1px solid #e2e8f0;">
            <h2 style="color:#1e40af; margin-top: 0;">{titulo}</h2>
            <hr style="border: 0.5px solid #f1f5f9;">
            <div style="color:#334155; line-height:1.6; font-size: 16px;">
                {conteudo_html}
            </div>
            <div style="margin-top: 30px; text-align: center;">
                <p style="font-size: 12px; color: #94a3b8;">Role para cima e clique no botão 'Fechar' do sistema para retornar.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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

    /* CONTAINER DO GIF HIGH-TECH */
    .high-tech-container {
        display: flex; justify-content: center; align-items: center; 
        margin: 20px 0; border-radius: 20px; overflow: hidden;
    }
       .modal-overlay {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(15, 23, 42, 0.7); display: flex;
        justify-content: center; align-items: center; z-index: 9999;
    }
    .modal-content {
        background: white; padding: 40px; border-radius: 24px;
        max-width: 800px; width: 90%; max-height: 80vh; overflow-y: auto;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3); position: relative;
    }
    .close-modal {
        position: absolute; top: 20px; right: 20px; cursor: pointer;
        font-size: 24px; font-weight: bold; color: #64748b;
    }     

</style>
""", unsafe_allow_html=True)

# --- 4. TELA DE LOGIN (SEGURANÇA CORPORATIVA) ---
def render_auth():
    st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1.4, 1])
    with col_login:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>TECHNOBOLT HUB</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#64748b; margin-bottom:40px; letter-spacing:1px;'>SISTEMA DE GOVERNANÇA COGNITIVA</p>", unsafe_allow_html=True)
        
        user_id = st.text_input("Identificador de Operador", placeholder="Usuário")
        user_key = st.text_input("Chave de Acesso Segura", type="password", placeholder="Senha")
        
        if st.button("AUTENTICAR NO HUB"):
            banco_users = {"admin": "admin", "jackson.antonio": "teste@2025", "luiza.trovao": "teste@2025"}
            if user_id in banco_users and banco_users[user_id] == user_key:
                st.session_state.logged_in = True
                st.session_state.user_atual = user_id
                st.session_state.login_time = time.time()
                st.session_state.uso_sessao = {} # Inicia rastreio
                
                # Relatório de Login
                agora = time.strftime('%H:%M:%S do dia %d/%m/%Y')
                enviar_notificacao_email("Relatório de Login", f"Usuário {user_id} acessou o sistema às {agora}.")
                
                st.rerun()

if not st.session_state.logged_in:
    render_auth()
    st.stop()

# --- 5. MOTOR DE INTELIGÊNCIA COM PROMPTS DE ELITE E FAILOVER PENTACAMADA ---
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

def call_technobolt_ai(prompt, attachments=None, system_context="default"):
    """
    Executa a requisição injetando o DNA Corporativo e aplicando Prompts de Consultoria Sênior.
    Segue frameworks: McKinsey 7S, Porter, MECE e RACI.
    """
    p = st.session_state.perfil_cliente
    dna_context = (
        f"DNA DA EMPRESA USUÁRIA:\n"
        f"- Empresa: {p['nome_empresa']}\n"
        f"- Setor: {p['setor']}\n"
        f"- Missão: {p['missao']}\n"
        f"- Valores: {p['valores']}\n"
        f"- Tom de Voz: {p['tom_voz']}\n\n"
    )

    # REVISÃO E APRIMORAMENTO DOS PROMPTS DE ELITE
    contexts = {
        "mckinsey": (
            "Aja como um Sócio Sênior da McKinsey & Company. Sua tarefa é auditar o documento anexo. "
            "Use o framework 'McKinsey 7S' e garanta o princípio MECE. "
            "ENTREGA: 1. Resumo Executivo Estratégico. 2. Diagnóstico Técnico de Gargalos. "
            "3. Matriz de Risco (Impacto Financeiro vs Probabilidade). 4. Plano de Ação 30-60-90 dias. "
            "Foque em ROI, Eficiência Operacional e Mitigação de Riscos Críticos."
        ),
        "email": (
            "Aja como um especialista em Diplomacia Corporativa e Comunicação Executiva. "
            "Seu objetivo é redigir uma comunicação de alto impacto. "
            "DIRETRIZES: 1. Assunto magnético e profissional. 2. Estabelecimento imediato de valor. "
            "3. Chamada para ação (CTA) clara e diplomática. 4. Uso do DNA da empresa no tom de voz. "
            "Evite clichês corporativos. Seja conciso e autoritário."
        ),
        "briefing": (
            "Aja como um Diretor de Inteligência Competitiva. Realize um scan profundo de mercado. "
            "Aplique as '5 Forças de Porter' e Análise 'PESTEL'. "
            "ENTREGA: Dossiê de Inteligência sobre tendências disruptivas, análise de rivais e ameaças de churn. "
            "Identifique lacunas de oportunidade baseadas no DNA da nossa empresa."
        ),
        "ata": (
            "Aja como um Secretário de Governança de Conselhos Administrativos Sênior. "
            "Formalize uma Ata de Reunião com precisão técnica absoluta. "
            "ESTRUTURA: 1. Cabeçalho de Governança. 2. Pautas e Deliberações MECE. 3. Matriz de Responsabilidade (RACI). "
            "4. Cronograma de Follow-up. Use linguagem jurídico-administrativa de alto nível."
        ),
        "default": (
            "Você é o Motor de Inteligência Estratégica TechnoBolt. Postura de Consultoria Sênior. "
            "Respostas técnicas, estruturadas em Markdown e focadas em resultados operacionais."
        )
    }

    final_sys_instr = dna_context + contexts.get(system_context, contexts["default"])

    for model_name in MODEL_FAILOVER_LIST:
        try:
            model = genai.GenerativeModel(model_name, system_instruction=final_sys_instr)
            payload = [prompt] + attachments if attachments else prompt
            response = model.generate_content(payload)
            return response.text, model_name
        except Exception:
            try:
                model_fb = genai.GenerativeModel(model_name)
                full_p = f"{final_sys_instr}\n\nSOLICITAÇÃO: {prompt}"
                response = model_fb.generate_content([full_p] + attachments if attachments else full_p)
                return response.text, model_name
            except:
                continue
    return "⚠️ Motores de IA Offline. Contate a governança.", "OFFLINE"

def export_docx(title, content):
    """Gera documentos Microsoft Word com formatação corporativa e selo de auditoria."""
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
        status_label += " <span class='admin-label'>PRIVILEGED ACCESS</span>"
    st.markdown(f"**OPERADOR:** <span class='status-badge'>{status_label}</span>", unsafe_allow_html=True)

with head_r:
    st.markdown('<div class="logout-zone">', unsafe_allow_html=True)
    if st.button("🚪 Sair do Hub"):
        protocol_logout()
    st.markdown('</div>', unsafe_allow_html=True)

menu_navegacao = [
    "🏠 Centro de Comando", 
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

# --- 7. MÓDULOS DE FUNCIONALIDADES INTEGRAIS (550+ LINHAS) ---

# PERFIL DO CLIENTE (DNA CORPORATIVO)
if "👤 Perfil" in escolha:
    st.markdown('<div class="main-card"><h2>👤 Perfil do Cliente (DNA Corporativo)</h2><p>Defina o contexto mestre para que todos os prompts da IA sejam personalizados para sua empresa.</p></div>', unsafe_allow_html=True)
    with st.form("form_perfil_elite"):
        c1, c2 = st.columns(2)
        nome = c1.text_input("Nome da Empresa:", value=st.session_state.perfil_cliente["nome_empresa"])
        setor = c2.text_input("Setor de Atuação:", value=st.session_state.perfil_cliente["setor"])
        missao = st.text_area("Missão e Propósito:", value=st.session_state.perfil_cliente["missao"])
        valores = st.text_input("Valores Principais (separados por vírgula):", value=st.session_state.perfil_cliente["valores"])
        tom = st.selectbox("Tom de Voz Desejado:", ["Executivo e Autoritário", "Diplomático e Analítico", "Inovador e Ágil", "Técnico e Preciso"])
        
        if st.form_submit_button("SALVAR DNA CORPORATIVO"):
            st.session_state.perfil_cliente = {
                "nome_empresa": nome, "setor": setor, "missao": missao, 
                "valores": valores, "tom_voz": tom
            }
            st.success("DNA Corporativo injetado com sucesso! Todos os módulos agora operam sob este contexto.")
            st.rerun()

# DASHBOARD CENTRAL COM GIF HIGH-TECH
elif "🏠 Centro" in escolha:
    st.markdown('<div class="main-card" style="max-width:100%;"><h1>Command Center</h1><p>Monitoria de Soberania Digital e Redundância Ativa de Motores.</p></div>', unsafe_allow_html=True)
    
    # GIF HIGH-TECH SOLICITADO
    st.markdown("""
    <div class="high-tech-container">
        <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXlsaTYwaDZkeGc2MjMxcXk4MWJjMGtwcHEwNTZ6dHFkaXV0NzNxbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eljCVpMrhepUSgZaVP/giphy.gif" alt="Tecnologia Girando">
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("IA Engine", "Soberana", "Redundância On")
    c2.metric("Sessão", st.session_state.user_atual.capitalize(), "Protegida")
    c3.metric("DNA Ativo", st.session_state.perfil_cliente["nome_empresa"])

# ANALISADOR MCKINSEY
elif "📁 Analisador McKinsey" in escolha:
    st.markdown('<div class="main-card"><h2>📁 Analisador de Documentos McKinsey</h2><p>Auditoria técnica profunda sob o DNA estratégico da empresa.</p></div>', unsafe_allow_html=True)
    arquivo_up = st.file_uploader("Submeter Documento (PDF/DOCX/TXT):", type=['pdf', 'docx', 'txt'])
    if arquivo_up and st.button("REVISAR"):
        registrar_evento("Analisador McKinsey")
        with st.spinner("IA Processando sob padrão McKinsey de excelência..."):
            if arquivo_up.type == "application/pdf":
                dados_ia = [{"mime_type": "application/pdf", "data": arquivo_up.read()}]
            else:
                texto_raw = extrair_texto_docx(arquivo_up) if arquivo_up.name.endswith('docx') else arquivo_up.read().decode(errors="ignore")
                dados_ia = [texto_raw]
            
            res_ia, mod_ia = call_technobolt_ai("Audite este documento focando em ROI e riscos.", dados_ia, system_context="mckinsey")
            mostrar_popup(f"Auditoria McKinsey - {mod_ia}", res_ia)
            st.download_button("📥 Baixar Relatório", data=export_docx("Auditoria McKinsey", res_ia), file_name=f"Auditoria_{arquivo_up.name}.docx")

# EMAIL INTEL (LOTE)
elif "📧 Email Intel" in escolha:
    st.markdown('<div class="main-card"><h2>📧 Email Intel: Auditoria em Lote</h2><p>Processamento massivo de e-mails para triagem executiva.</p></div>', unsafe_allow_html=True)
    emails = st.file_uploader("Upload Emails (PDF):", type=['pdf'], accept_multiple_files=True)
    if emails and st.button("PROCESSAR LOTE DE AUDITORIA"):
        registrar_evento("Email Intel (Lote)")
        with st.spinner("Auditando lote de mensagens..."):
            relatorio_lote = ""
            for email_pdf in emails:
                res_email, _ = call_technobolt_ai("Resuma tecnicamente e rascunhe a resposta ideal.", [{"mime_type": "application/pdf", "data": email_pdf.read()}], system_context="email")
                relatorio_lote += f"<h3>Email: {email_pdf.name}</h3>{res_email}<hr>"
            mostrar_popup("Relatório de Auditoria em Lote", relatorio_lote)

# GERADOR DE EMAILS COM BARRA DE FORMALIDADE
elif "✉️ Gerador de Emails" in escolha:
    st.markdown('<div class="main-card"><h2>✉️ Gerador de Emails de Alto Impacto</h2></div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    cargo_e = ca.text_input("Seu Cargo para Assinatura:")
    dest_e = cb.text_input("Cargo do Destinatário:")
    formalidade = st.select_slider("Nível de Formalidade Corporativa", 
                                   options=["Casual", "Corporativo", "Executivo", "Rígido/Diplomático"], 
                                   value="Executivo")
    contexto_e = st.text_area("Objetivo da Mensagem ou Tópicos Críticos:")
    if st.button("GERAR E-MAIL EXECUTIVO"):
        registrar_evento("Gerador de Emails")
        with st.spinner("IA Redigindo..."):
            p_email = f"Como {cargo_e}, escreva um email para {dest_e} sobre {contexto_e}. Formalidade: {formalidade}."
            res_email, _ = call_technobolt_ai(p_email, system_context="email")
            mostrar_popup("Rascunho Executivo Gerado", res_email)
            st.download_button("📥 Baixar Word", data=export_docx("Email Gerado", res_email), file_name="Rascunho_Email.docx")

# BRIEFING ESTRATÉGICO
elif "🧠 Briefing" in escolha:
    st.markdown('<div class="main-card"><h2>🧠 Briefing Estratégico & Radar 2026</h2></div>', unsafe_allow_html=True)
    e_alvo = st.text_input("Empresa ou Setor para Análise de Inteligência:")
    if st.button("EXECUTAR BRIEFING ESTRATÉGICO"):
        registrar_evento("Briefing Estratégico")
        with st.spinner("Escaneando mercado..."):
            res_brief, mod = call_technobolt_ai(f"Gere um briefing estratégico completo para {e_alvo}.", system_context="briefing")
            mostrar_popup(f"Briefing Estratégico - {e_alvo}", res_brief)

# GESTOR DE ATAS COM RACI
elif "📝 Gestor de Atas" in escolha:
    st.markdown('<div class="main-card"><h2>📝 Gestor de Atas de Governança</h2></div>', unsafe_allow_html=True)
    notas_r = st.text_area("Notas da Reunião ou Transcrição:", height=280)
    if st.button("FORMALIZAR ATA DE DIRETORIA"):
        registrar_evento("Gestor de Atas")
        with st.spinner("Formatando ata..."):
            res_ata, _ = call_technobolt_ai(f"Formalize as seguintes notas em Ata de Diretoria: {notas_r}", system_context="ata")
            mostrar_popup("Ata de Diretoria Formalizada", res_ata)
            st.download_button("📥 Baixar Ata Word", data=export_docx("Ata Oficial", res_ata), file_name="Ata_Oficial.docx")

# MERCADO & CHURN
elif "📈 Mercado & Churn" in escolha:
    st.markdown('<div class="main-card"><h2>📈 Inteligência de Mercado & Churn</h2></div>', unsafe_allow_html=True)
    tab_rival, tab_churn = st.tabs(["🔍 Radar de Concorrência", "⚠️ Risco de Churn"])
    with tab_rival:
        rival_n = st.text_input("Empresa para Análise:")
        if st.button("ANALISAR ESTRATÉGIA"):
            registrar_evento("Análise de Rival")
            with st.spinner("Analisando concorrência..."):
                res_r, _ = call_technobolt_ai(f"Análise competitiva profunda de: {rival_n}", system_context="briefing")
                mostrar_popup(f"Radar de Concorrência: {rival_n}", res_r)
    with tab_churn:
        feed_c = st.text_area("Feedback do Cliente para Análise de Risco:");
        if st.button("CALCULAR RISCO DE PERDA"):
            registrar_evento("Cálculo de Churn")
            with st.spinner("Avaliando risco..."):
                res_c, _ = call_technobolt_ai(f"Avalie o risco de churn baseado no feedback: {feed_c}")
                mostrar_popup("Diagnóstico de Risco (Churn)", res_c)

# RELATÓRIO MASTER
elif "📊 Relatório Master" in escolha:
    st.markdown('<div class="main-card"><h2>📊 Relatório Master de Diretoria</h2><p>Dossiê consolidado de KPIs e eventos da semana.</p></div>', unsafe_allow_html=True)
    kpis = st.text_area("Fatos, métricas e decisões da semana:")
    if st.button("GERAR DOSSIÊ MASTER"):
        registrar_evento("Relatório Master")
        with st.spinner("Consolidando dados..."):
            res_master, _ = call_technobolt_ai(f"Gere um Relatório Master consolidando: {kpis}.", system_context="ata")
            mostrar_popup("Relatório Master Consolidado", res_master)
            st.download_button("📥 Baixar Relatório", data=export_docx("Relatório Master", res_master), file_name="Master_Dossie.docx")

# --- 8. RODAPÉ DE GOVERNANÇA ---
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
st.caption(f"TechnoBolt Solutions © 2026 | Elite Hub Edition v1.0 | Operador: {st.session_state.user_atual.upper()}")