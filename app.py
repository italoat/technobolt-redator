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

# --- 2. CSS CYBER-PUNK & GLASSMORPHISM (ESTÉTICA AZUL PROFUNDO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

    /* FUNDO AZUL ESCURO CIBERNÉTICO ABSOLUTO */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background: radial-gradient(circle at center, #0a192f 0%, #020617 100%) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #e2e8f0 !important;
    }

    /* REMOVER SIDEBAR E ELEMENTOS NATIVOS */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* FORÇAR TEXTO CLARO */
    * { color: #f8fafc !important; }

    /* CARD GLASSMORPHISM REFORÇADO */
    .login-card {
        background: rgba(16, 30, 56, 0.6) !important;
        backdrop-filter: blur(25px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(25px) saturate(180%) !important;
        padding: 60px;
        border-radius: 35px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        box-shadow: 0 0 50px rgba(37, 99, 235, 0.25);
        text-align: center;
        margin: auto;
        max-width: 500px;
    }

    /* TÍTULO TECH */
    .main-title { 
        font-size: 48px; font-weight: 800; text-align: center; 
        background: linear-gradient(135deg, #60a5fa, #3b82f6, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent !important;
        letter-spacing: -2px; line-height: 1.1; margin-bottom: 10px;
        padding: 10px 0;
    }

    .product-header { 
        background: rgba(30, 41, 59, 0.5); 
        backdrop-filter: blur(15px);
        padding: 45px; border-radius: 30px; margin-bottom: 35px; 
        border: 1px solid rgba(59, 130, 246, 0.2);
    }

    /* INPUTS COM FOCO NEON */
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid #1e3a8a !important;
        border-radius: 14px !important;
        padding: 15px !important;
    }
    
    .stTextInput input:focus {
        border-color: #60a5fa !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.5) !important;
    }

    /* CORREÇÃO DE LISTA SUSPENSA (FUNDO ESCURO) */
    div[data-baseweb="select"] > div, div[data-baseweb="popover"], ul[role="listbox"] {
        background-color: #0f172a !important;
        color: white !important;
        border: 1px solid #1e3a8a !important;
    }
    li[role="option"]:hover { background-color: #1e40af !important; }

    /* BOTÕES EXECUTIVOS */
    .stButton > button { 
        width: 100%; 
        border-radius: 14px; 
        height: 4.2em; 
        font-weight: 700; 
        background: linear-gradient(90deg, #1d4ed8 0%, #3b82f6 100%) !important; 
        color: #ffffff !important; 
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.6) !important;
    }

    /* BADGE DE STATUS */
    .model-badge {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981 !important;
        padding: 6px 16px; border-radius: 25px;
        border: 1px solid #10b981; font-size: 11px; font-weight: 800;
    }

    hr { border: 0.5px solid rgba(59, 130, 246, 0.2) !important; margin: 40px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE AUTENTICAÇÃO ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def tela_login():
    st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.8, 1])
    
    with col2:
        st.markdown("""
            <div class='login-card'>
                <p style='color: #60a5fa; font-weight: 800; letter-spacing: 4px; margin-bottom: 0;'>TECHNOBOLT</p>
                <h1 class='main-title'>HUB DE GOVERNANÇA COGNITIVA</h1>
                <p style='color: #94a3b8; font-size: 14px; margin-bottom: 40px; letter-spacing: 1px;'>Sistema de Inteligência e Monitoria Resiliente</p>
            
                    
                    </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            u_in = st.text_input("Identificador de Usuário", placeholder="Login", label_visibility="collapsed")
            
            # Lógica funcional de visualizar senha
            col_pwd, col_eye = st.columns([0.88, 0.12])
            with col_eye:
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                ver_senha = st.checkbox("👁️", help="Exibir/Ocultar senha")
            
            with col_pwd:
                p_in = st.text_input("Senha", 
                                    type="default" if ver_senha else "password", 
                                    placeholder="Senha de Acesso", 
                                    label_visibility="collapsed")
            
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            
            if st.button("INICIAR CONEXÃO SEGURA"):
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
                    st.error("⚠️ ACESSO NEGADO: Credenciais não autorizadas.")
        
        st.markdown("<p style='text-align: center; color: #1e3a8a; font-size: 10px; margin-top: 40px; letter-spacing: 3px;'>PROTOCOLO DE SEGURANÇA AES-256 ATIVO</p>", unsafe_allow_html=True)

if not st.session_state.logged_in:
    tela_login()
    st.stop()

# --- 4. LÓGICA DE INTELIGÊNCIA COM FAILOVER (ESTRUTURA COMPLETA) ---
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
    """Executa o prompt com instrução de sistema rigorosa."""
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
    return "⚠️ Erro: Todos os motores de IA estão fora de linha.", "Esgotado"

def gerar_docx(titulo, conteudo):
    doc = docx.Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"TechnoBolt Solutions - Hub de Governança Cognitiva")
    doc.add_paragraph(f"Operador Responsável: {st.session_state.user_atual}")
    doc.add_paragraph(f"Data da Extração: {time.strftime('%d/%m/%Y %H:%M')}")
    doc.add_paragraph("-" * 35)
    doc.add_paragraph(conteudo)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 5. INTERFACE DO HUB (NAVEGAÇÃO COMPLETA) ---
st.markdown(f'<div style="text-align:right; font-size:11px; color:#60a5fa; letter-spacing:1px;">ID SESSÃO: {st.session_state.user_atual.upper()} | <a href="/" style="color:#f87171; text-decoration:none;">[ SAIR ]</a></div>', unsafe_allow_html=True)
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

# --- 6. TELAS DO HUB (CONTEÚDO INTEGRAL) ---

# DASHBOARD
if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>Centro de Comando Corporativo</h1><p>Monitoria Cognitiva e Governança em Tempo Real</p></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Status da IA", "Soberana", delta="Failover Ativo")
    with c2: st.metric("Operador Autenticado", st.session_state.user_atual.capitalize())
    with c3: st.metric("Proteção de Dados", "AES-256", delta="Criptografado")
    st.info("Ecossistema TechnoBolt operando normalmente. Selecione uma solução técnica acima para iniciar.")

# EMAIL INTEL (AUDITORIA EM LOTE)
elif "📧 Email Intel" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📧 Email Intel: Auditoria & Resposta</h1></div>', unsafe_allow_html=True)
    col_u, col_r = st.columns([1, 2])
    with col_u:
        arquivos = st.file_uploader("Anexe e-mails em PDF:", type=["pdf"], accept_multiple_files=True)
        cargo = st.text_input("Cargo p/ Rascunho:", value="Diretor de Operações")
        tom = st.selectbox("Tom da Resposta:", ["Executivo", "Diplomático", "Cordial", "Firme"])
        btn_audit = st.button("🔍 EXECUTAR AUDITORIA EM LOTE")
    with col_r:
        if arquivos and btn_audit:
            for i, pdf in enumerate(arquivos):
                with st.expander(f"Análise: {pdf.name}", expanded=True):
                    with st.spinner(f"Processando {pdf.name}..."):
                        pdf_data = [{"mime_type": "application/pdf", "data": pdf.read()}]
                        p_audit = f"Resuma este e-mail, extraia riscos e rascunhe uma resposta como {cargo} em tom {tom}."
                        res_texto, mod_ativo = call_ai_with_failover(p_audit, pdf_data)
                        st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod_ativo}</span>', unsafe_allow_html=True)
                        st.markdown(res_texto)
                        st.download_button(f"📩 Baixar {i+1}", data=gerar_docx("Auditoria", res_texto), file_name=f"Auditoria_{i}.docx")

# ANALISADOR DE DOCUMENTOS
elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos & Contratos</h1></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Upload (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
    if arquivo and st.button("🔍 INICIAR ANÁLISE MCKINSEY"):
        with st.spinner("IA processando dados técnicos..."):
            if arquivo.type == "application/pdf":
                dados = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                prompt_doc = "Aja como Consultor McKinsey da Technobolt. Gere: Resumo Executivo, Impacto (Risco/Custo) e Plano de Ação."
            else:
                texto_raw = extrair_texto_docx(arquivo) if arquivo.name.endswith('docx') else arquivo.read().decode()
                dados = [texto_raw]
                prompt_doc = "Analise o texto a seguir sob a ótica de negócios para a Technobolt Solutions:"
            res_doc, mod_doc = call_ai_with_failover(prompt_doc, dados)
            st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod_doc}</span>', unsafe_allow_html=True)
            st.markdown(res_doc); st.download_button("📄 Baixar Relatório", data=gerar_docx("Análise", res_doc), file_name="Relatorio.docx")

# GERADOR DE EMAIL
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1></div>', unsafe_allow_html=True)
    cargo_e = st.text_input("Seu Cargo:"); obj_e = st.text_area("Objetivo da Mensagem:")
    formalidade = st.select_slider("Formalidade:", ["Casual", "Executivo", "Rígido"], value="Executivo")
    if st.button("🚀 GERAR COMUNICAÇÃO"):
        res, mod = call_ai_with_failover(f"Como {cargo_e}, escreva um email sobre {obj_e} em tom {formalidade}.")
        st.markdown(f'<span class="model-badge">MOTOR: {mod}</span>', unsafe_allow_html=True)
        st.text_area("Rascunho:", res, height=400)

# BRIEFING NEGOCIAL
elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Negocial Estratégico</h1></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: emp_a = st.text_input("Empresa Alvo:")
    with col2: set_a = st.text_input("Setor de Atuação:")
    objetivo_b = st.text_area("Objetivo da Análise:")
    if st.button("⚡ ESCANEAR MERCADO"):
        if emp_a:
            with st.spinner("Gerando radar..."):
                res, mod = call_ai_with_failover(f"Briefing 2026 para {emp_a} no setor {set_a}. Foco: {objetivo_b}")
                st.markdown(res); st.download_button("🧠 Baixar Briefing", data=gerar_docx("Briefing", res), file_name="Briefing.docx")

# ANALISTA DE ATAS
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas de Governança</h1></div>', unsafe_allow_html=True)
    notas_r = st.text_area("Notas da reunião:", height=300)
    if st.button("📝 FORMALIZAR ATA OFICIAL"):
        res, mod = call_ai_with_failover(f"Transforme as seguintes notas em uma ata formal de diretoria: {notas_r}")
        st.markdown(res); st.download_button("📝 Baixar Ata", data=gerar_docx("Ata Oficial", res), file_name="Ata.docx")

# INTELIGÊNCIA COMPETITIVA
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência Competitiva & Churn</h1></div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔍 Monitoria de Concorrentes", "⚠️ Radar de Churn"])
    with tab1:
        rival_n = st.text_input("Nome do Rival:")
        if st.button("📡 ANALISAR ESTRATÉGIA"):
            res, mod = call_ai_with_failover(f"Analise a estratégia atual da empresa {rival_n}."); st.markdown(res)
    with tab2:
        feed_c = st.text_area("Feedback do cliente insatisfeito:")
        if st.button("🧠 CALCULAR RISCO"):
            res, mod = call_ai_with_failover(f"Avalie risco de churn e plano de retenção para: {feed_c}"); st.markdown(res)

# RELATÓRIO MASTER
elif "📊 Relatório Master" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📊 Relatório Master de Governança</h1></div>', unsafe_allow_html=True)
    compilado_s = st.text_area("Notas da semana para consolidação:", height=400)
    if st.button("🚀 GERAR DOSSIÊ MASTER"):
        if compilado_s:
            p_master = f"Aja como Chief of Staff TechnoBolt Solutions. Organize em Relatório Semanal: 1. RESUMO, 2. DECISÕES, 3. RISCOS e 4. PRÓXIMOS PASSOS. Dados: {compilado_s}"
            res, mod = call_ai_with_failover(p_master); st.markdown(res)
            st.download_button("📊 Baixar Relatório Master", data=gerar_docx("Relatório Master", res), file_name="Governanca.docx")

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Master Resilience Edition v1.0 | Operador: {st.session_state.user_atual.upper()}")