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

# --- 2. CSS UX-ADVANCED (ESTÉTICA CIBERNÉTICA & ZERO WHITE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

    /* FUNDO AZUL ESCURO PROFUNDO SEM MANCHAS */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background: radial-gradient(circle at center, #0a192f 0%, #020617 100%) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #e2e8f0 !important;
    }

    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* FORÇAR CORES CLARAS */
    * { color: #f8fafc !important; }

    /* CENTRALIZAÇÃO ABSOLUTA DA TELA DE LOGIN */
    .st-emotion-cache-12w0qpk { 
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* CARD DE LOGIN GLASSMORPHISM UX-FOCUSED */
    .login-card {
        background: rgba(16, 30, 56, 0.45);
        backdrop-filter: blur(35px);
        -webkit-backdrop-filter: blur(35px);
        padding: 65px;
        border-radius: 45px;
        border: 1px solid rgba(59, 130, 246, 0.25);
        box-shadow: 0 50px 100px rgba(0, 0, 0, 0.7);
        text-align: center;
        width: 100%;
        max-width: 580px;
        margin: auto;
    }

    /* TÍTULO TECH COM GRADIENTE */
    .main-title { 
        font-size: 44px; font-weight: 800; text-align: center; 
        background: linear-gradient(135deg, #60a5fa, #3b82f6, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent !important;
        letter-spacing: -2px; line-height: 1.1; margin-bottom: 25px;
    }

    .product-header { 
        background: rgba(16, 30, 56, 0.5); 
        backdrop-filter: blur(20px);
        padding: 50px; border-radius: 35px; margin-bottom: 40px; 
        border: 1px solid rgba(59, 130, 246, 0.2);
    }

    /* INPUTS MODERNOS (UX PREMIUM) */
    .stTextInput > div > div > input {
        background-color: rgba(15, 23, 42, 0.7) !important;
        color: #ffffff !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 20px !important;
        padding: 20px 25px !important;
        height: 65px !important;
        font-size: 17px !important;
        transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.5) !important;
        background-color: rgba(15, 23, 42, 0.9) !important;
    }

    /* BOTÃO TECH SEM FUNDO PRETO NO TEXTO */
    .stButton > button { 
        width: 100%; 
        border-radius: 20px; 
        height: 4.5em; 
        font-weight: 700; 
        background: linear-gradient(90deg, #1d4ed8 0%, #3b82f6 100%) !important; 
        color: #ffffff !important; 
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .stButton > button div[data-testid="stMarkdownContainer"], 
    .stButton > button p {
        background: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
        margin: 0 !important;
        padding: 0 !important;
        text-shadow: none !important;
    }

    .stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(59, 130, 246, 0.6) !important;
    }

    /* LISTA SUSPENSA E SELECTBOX DARK */
    div[data-baseweb="select"] > div, div[data-baseweb="popover"], ul[role="listbox"] {
        background-color: #0f172a !important;
        color: white !important;
        border: 1px solid #1e3a8a !important;
    }

    /* BADGE DE STATUS */
    .model-badge {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981 !important;
        padding: 8px 18px; border-radius: 25px;
        border: 1px solid #10b981; font-size: 11px; font-weight: 800;
    }

    hr { border: 0.5px solid rgba(59, 130, 246, 0.2) !important; margin: 45px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE AUTENTICAÇÃO ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def tela_login():
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    st.markdown("""
        <p style='color:#60a5fa;font-weight:700;letter-spacing:4px;font-size:11px;margin-bottom:6px;'>
            SISTEMA ATIVO
        </p>
        <h1 class='main-title'>TECHNOBOLT IA</h1>
        <p class='login-subtitle'>
            HUB DE GOVERNANÇA COGNITIVA<br>
            Autenticação segura requerida
        </p>
    """, unsafe_allow_html=True)

    u_in = st.text_input(
        "USUÁRIO",
        placeholder="Identidade do operador",
        label_visibility="collapsed"
    )

    col_pwd = st.columns([0.85, 0.15])

    with col_pwd:
        p_in = st.text_input(
            "SENHA",
            type="password",
            placeholder="Chave criptográfica",
            label_visibility="collapsed"
        )

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    if st.button("INICIAR CONEXÃO"):
        usuarios = {
            "admin": "admin",
            "jackson.antonio": "teste@2025",
            "luiza.trovao": "teste@2025",
            "usuario.teste": "teste@2025"
        }
        if u_in in usuarios and usuarios[u_in] == p_in:
            st.session_state.logged_in = True
            st.session_state.user_atual = u_in
            st.rerun()
        else:
            st.error("Acesso negado. Credenciais inválidas.")

    st.markdown("""
        <p style='margin-top:32px;font-size:10px;color:#1e3a8a;letter-spacing:3px;'>
            AES-256 • ZERO TRUST • SESSION LOCK
        </p>
    """, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    tela_login()
    st.stop()

# --- 4. LÓGICA DE INTELIGÊNCIA COM FAILOVER (ESTRUTURA INTEGRAL) ---
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

def call_ai_with_failover(prompt, content_list=None):
    """Executa o motor de inteligência com suporte a redundância."""
    sys_instr = (
        "Você é o motor de inteligência da TechnoBolt Solutions. "
        "Sua saída deve ser estritamente profissional e técnica. "
        "PROIBIDO: Usar frases como 'Aqui está', 'Entendido', 'Como solicitado' ou saudações. "
        "ENTREGA: Responda diretamente com o conteúdo estruturado em Markdown."
    )
    
    for model_id in MODEL_LIST:
        try:
            model = genai.GenerativeModel(model_id, system_instruction=sys_instr)
            if content_list:
                response = model.generate_content([prompt] + content_list)
            else:
                response = model.generate_content(prompt)
            return response.text, model_id
        except Exception as e:
            if "429" in str(e):
                continue
            try:
                model_fb = genai.GenerativeModel(model_id)
                full_prompt = f"{sys_instr}\n\nSOLICITAÇÃO: {prompt}"
                response = model_fb.generate_content([full_prompt] + content_list if content_list else full_prompt)
                return response.text, model_id
            except:
                continue
    return "⚠️ Erro Crítico: Motores de IA fora de operação.", "Esgotado"

def gerar_docx(titulo, conteudo):
    doc = docx.Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"TechnoBolt Solutions - Hub de Governança")
    doc.add_paragraph(f"Operador Responsável: {st.session_state.user_atual}")
    doc.add_paragraph(f"Data da Extração: {time.strftime('%d/%m/%Y %H:%M')}")
    doc.add_paragraph("-" * 35)
    doc.add_paragraph(conteudo)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 5. INTERFACE DO HUB (NAVEGAÇÃO COMPLETA) ---
st.markdown(f'<div style="text-align:right; font-size:11px; color:#60a5fa; letter-spacing:1px;">OPERADOR: {st.session_state.user_atual.upper()} | <a href="/" style="color:#f87171; text-decoration:none;">LOGOUT</a></div>', unsafe_allow_html=True)
st.markdown('<div class="main-title" style="font-size: 32px; padding:0;">TechnoBolt IA Hub</div>', unsafe_allow_html=True)

menu_opcoes = [
    "🏠 Dashboard Inicial", 
    "📁 Analisador de Documentos & Contratos",
    "📧 Email Intel: Auditoria em Lote",
    "✉️ Gerador de Email Inteligente", 
    "🧠 Briefing Negocial Estratégico", 
    "📝 Analista de Atas de Governança",
    "📈 Inteligência Competitiva & Churn",
    "📊 Relatório Master de Governança"
]
menu_selecionado = st.selectbox("Seletor de Módulo", menu_opcoes, label_visibility="collapsed")
st.markdown("<hr>", unsafe_allow_html=True)

# --- 6. TELAS DO HUB (CONTEÚDO COMPLETO) ---

if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>Centro de Comando Corporativo</h1><p>Monitoria Cognitiva e Governança em Tempo Real</p></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("IA Status", "Online", delta="Soberana")
    with c2: st.metric("Operador", st.session_state.user_atual.capitalize())
    with c3: st.metric("Proteção", "Ativa", delta="AES-256")
    st.info("O Terminal TechnoBolt está operacional. Selecione um módulo para processamento de dados.")

elif "📧 Email Intel" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📧 Email Intel: Auditoria & Resposta</h1></div>', unsafe_allow_html=True)
    col_u, col_r = st.columns([1, 2])
    with col_u:
        arquivos = st.file_uploader("Upload de Emails (PDF):", type=["pdf"], accept_multiple_files=True)
        cargo = st.text_input("Seu Cargo p/ Resposta:", value="Diretor")
        tom = st.selectbox("Tom da Comunicação:", ["Executivo", "Cordial", "Firme"])
        btn_audit = st.button("🔍 INICIAR AUDITORIA")
    with col_r:
        if arquivos and btn_audit:
            for i, pdf in enumerate(arquivos):
                with st.expander(f"Análise: {pdf.name}", expanded=True):
                    with st.spinner(f"Processando {pdf.name}..."):
                        pdf_data = [{"mime_type": "application/pdf", "data": pdf.read()}]
                        res, mod = call_ai_with_failover(f"Resuma e rascunhe resposta como {cargo} tom {tom}", pdf_data)
                        st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod}</span>', unsafe_allow_html=True)
                        st.markdown(res)
                        st.download_button(f"📩 Baixar {i}", data=gerar_docx("Auditoria", res), file_name=f"Auditoria_{i}.docx")

elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos & Contratos</h1></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Upload de Documento:", type=["pdf", "docx", "txt"])
    if arquivo and st.button("🔍 EXECUTAR ANÁLISE MCKINSEY"):
        with st.spinner("IA processando dados técnicos..."):
            if arquivo.type == "application/pdf":
                dados = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                prompt_doc = "Aja como Consultor McKinsey da Technobolt. Gere: Resumo Executivo, Impacto e Plano de Ação."
            else:
                texto_raw = extrair_texto_docx(arquivo) if arquivo.name.endswith('docx') else arquivo.read().decode()
                dados = [texto_raw]
                prompt_doc = "Analise este documento sob a ótica de negócios para a Technobolt Solutions:"
            res, mod = call_ai_with_failover(prompt_doc, dados)
            st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod}</span>', unsafe_allow_html=True)
            st.markdown(res); st.download_button("📄 Baixar Relatório", data=gerar_docx("Análise", res), file_name="Relatorio.docx")

elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1></div>', unsafe_allow_html=True)
    obj_e = st.text_area("Objetivo da Mensagem:"); fml = st.select_slider("Formalidade:", ["Casual", "Executivo", "Rígido"])
    if st.button("🚀 GERAR COMUNICAÇÃO"):
        res, mod = call_ai_with_failover(f"Escreva email sobre {obj_e} no tom {fml}")
        st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod}</span>', unsafe_allow_html=True)
        st.text_area("Rascunho:", res, height=400)

elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Negocial Estratégico</h1></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: emp_a = st.text_input("Empresa Alvo:")
    with col2: set_a = st.text_input("Setor:")
    obj_b = st.text_area("Objetivo da Análise:")
    if st.button("⚡ ESCANEAR MERCADO"):
        if emp_a:
            with st.spinner(f"Gerando briefing para {emp_a}..."):
                res, mod = call_ai_with_failover(f"Briefing 2026 para {emp_a} no setor {set_a}. Foco: {obj_b}")
                st.markdown(res); st.download_button("🧠 Baixar", data=gerar_docx(f"Briefing {emp_a}", res), file_name="Briefing.docx")

elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas de Governança</h1></div>', unsafe_allow_html=True)
    notas_r = st.text_area("Notas da reunião:", height=350)
    if st.button("📝 FORMALIZAR ATA"):
        res, mod = call_ai_with_failover(f"Transforme as seguintes notas em uma ata formal de diretoria: {notas_r}")
        st.markdown(res); st.download_button("📝 Baixar Ata", data=gerar_docx("Ata", res), file_name="Ata_Oficial.docx")

elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência & Churn</h1></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Monitoria de Rivais", "⚠️ Radar de Churn"])
    with t1:
        rival_n = st.text_input("Nome do Rival:")
        if st.button("📡 ANALISAR ESTRATÉGIA"):
            res, mod = call_ai_with_failover(f"Analise a estratégia competitiva atual da empresa {rival_n}."); st.markdown(res)
    with t2:
        feed_c = st.text_area("Feedback do cliente:");
        if st.button("🧠 CALCULAR RISCO"):
            res, mod = call_ai_with_failover(f"Avalie risco de churn e plano de retenção para: {feed_c}"); st.markdown(res)

elif "📊 Relatório Master" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📊 Relatório Master de Governança</h1></div>', unsafe_allow_html=True)
    compilado_s = st.text_area("Dados da semana para consolidação:", height=400)
    if st.button("🚀 GERAR DOSSIÊ MASTER"):
        if compilado_s:
            with st.spinner("IA TechnoBolt consolidando governança..."):
                p_master = f"Aja como Chief of Staff TechnoBolt Solutions. Organize: 1. Resumo, 2. Decisões, 3. Riscos, 4. Próximos Passos. Dados: {compilado_s}"
                res, mod = call_ai_with_failover(p_master); st.markdown(res)
                st.download_button("📊 Baixar Master", data=gerar_docx("Relatório Master", res), file_name="Governanca.docx")

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Master Resilience Edition v1.1 | Operador: {st.session_state.user_atual.upper()}")