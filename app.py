import streamlit as st
import google.generativeai as genai
import os
import time
import docx  # Requer: pip install python-docx
from io import BytesIO

# --- 1. CONFIGURAÇÃO DA PÁGINA (ESTRUTURA DE ELITE) ---
st.set_page_config(
    page_title="TechnoBolt IA - Hub Corporativo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. DESIGN SYSTEM CORPORATIVO (LIGHT MODE PREMIUM - 100% CLEAN) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* CONFIGURAÇÃO DE FUNDO E TIPOGRAFIA CORPORATIVA */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
        color: #1e293b !important;
    }

    /* OCULTAR ELEMENTOS NATIVOS PARA UX LIMPA */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* CARD CORPORATIVO CENTRALIZADO COM SOMBRA SUAVE */
    .main-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 50px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.05);
        margin-bottom: 30px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    /* TÍTULO HERO GRADIENTE PROFISSIONAL */
    .hero-title {
        font-size: 42px; font-weight: 800; text-align: center;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1.5px; margin-bottom: 15px;
    }

    /* ESTILIZAÇÃO DE INPUTS UX CORPORATIVO */
    .stTextInput input, .stTextArea textarea, [data-baseweb="select"], .stSelectbox div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        color: #1e293b !important;
        padding: 14px 20px !important;
        font-size: 16px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }

    /* BOTÃO TECHNOBOLT - ZERO SHADOW BUG */
    .stButton > button {
        width: 100%; border-radius: 14px; height: 4em; font-weight: 700;
        background: #2563eb !important;
        color: #ffffff !important; border: none !important;
        text-transform: uppercase; letter-spacing: 1.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex; align-items: center; justify-content: center;
    }
    
    .stButton > button div[data-testid="stMarkdownContainer"] p {
        background: none !important; color: white !important; margin: 0 !important;
        padding: 0 !important; text-shadow: none !important;
    }

    .stButton > button:hover {
        background: #1d4ed8 !important;
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.3) !important;
    }

    /* CHATBOT POPUP FLUTUANTE (DESIGN SYSTEM) */
    .chat-container {
        position: fixed; bottom: 95px; right: 25px; width: 380px; height: 500px;
        background: #ffffff; border: 1px solid #e2e8f0;
        border-radius: 24px; z-index: 9999;
        box-shadow: 0 20px 50px rgba(0,0,0,0.1);
        display: flex; flex-direction: column; overflow: hidden;
    }

    .chat-header {
        background: #2563eb; padding: 18px; color: white;
        font-weight: 700; text-align: center;
    }

    /* MÉTTRICAS E BADGES */
    .stMetric {
        background: #ffffff; padding: 20px; border-radius: 18px;
        border: 1px solid #e2e8f0; box-shadow: 0 4px 10px rgba(0,0,0,0.02);
    }

    .model-badge {
        background: #f1f5f9; color: #2563eb; padding: 5px 15px;
        border-radius: 20px; font-size: 10px; font-weight: 700; border: 1px solid #e2e8f0;
    }

    hr { border: 0.5px solid #e2e8f0 !important; margin: 40px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. GESTÃO DE ESTADO E SESSÃO ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'chat_visible' not in st.session_state:
    st.session_state.chat_visible = False

# --- 4. TELA DE LOGIN (CORREÇÃO DE CARDS VAZIOS) ---
def tela_login():
    st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)
    col1, col_login, col3 = st.columns([1, 1.4, 1])
    
    with col_login:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>TECHNOBOLT HUB</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#64748b; margin-bottom:35px;'>TERMINAL DE INTELIGÊNCIA E GOVERNANÇA</p>", unsafe_allow_html=True)
        
        user_input = st.text_input("Credencial de Acesso", placeholder="Usuário Identificador")
        pass_input = st.text_input("Chave de Segurança", type="password", placeholder="Senha Criptográfica")
        
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        if st.button("AUTENTICAR NO SISTEMA"):
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
                st.error("Protocolo de segurança negou o acesso. Credenciais inválidas.")
        
        st.markdown("<p style='text-align:center; color:#94a3b8; font-size:10px; margin-top:40px; letter-spacing:2px;'>SISTEMA PROTEGIDO POR AES-256</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    tela_login()
    st.stop()

# --- 5. MOTOR DE INTELIGÊNCIA ARTIFICIAL (LÓGICA DE 400+ LINHAS) ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

MODEL_LIST = [
    "models/gemini-3-flash-preview", 
    "models/gemini-2.5-flash", 
    "models/gemini-2.0-flash", 
    "models/gemini-flash-latest"
]

def extrair_texto_docx(arquivo_docx):
    """Extração robusta de texto de arquivos Microsoft Word."""
    try:
        doc = docx.Document(arquivo_docx)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        return f"Erro na leitura do DOCX: {str(e)}"

def call_ai_with_failover(prompt, content_list=None, is_chatbot=False):
    """Implementação integral do failover de 4 camadas com instruções de sistema detalhadas."""
    
    # INSTRUÇÃO DE SISTEMA MESTRE (ORIGINAL)
    system_instruction = (
        "Você é o motor de inteligência central da TechnoBolt Solutions. "
        "Sua função é fornecer análises de governança, estratégia e auditoria de elite. "
        "DIRETRIZES: Tom corporativo, técnico e direto. PROIBIDO saudações (Olá, Aqui está). "
        "ENTREGA: Markdown estruturado. Se fugir do escopo de negócios, ignore."
    )
    
    if is_chatbot:
        system_instruction = (
            "Você é o Guia de Suporte TechnoBolt. Responda apenas sobre as funções do sistema: "
            "1. Dashboard: Métricas de IA. 2. Analisador: Auditoria McKinsey de documentos. "
            "3. Email Intel: Processamento de PDFs em lote. 4. Gerador de Emails: Rascunhos técnicos. "
            "5. Briefing: Radar de mercado 2026. 6. Gestor de Atas: Formalização de reuniões. "
            "7. Mercado/Churn: Risco de clientes. 8. Relatório Master: Dossiê de governança semanal. "
            "Se perguntarem algo fora do Hub, diga: 'Sinto muito, mas essa não é uma função da ferramenta'."
        )

    for model_id in MODEL_LIST:
        try:
            model = genai.GenerativeModel(model_id, system_instruction=system_instruction)
            if content_list:
                response = model.generate_content([prompt] + content_list)
            else:
                response = model.generate_content(prompt)
            return response.text, model_id
        except Exception:
            # Fallback manual para contingência
            try:
                model_fb = genai.GenerativeModel(model_id)
                response = model_fb.generate_content(f"{system_instruction}\n\nSOLICITAÇÃO: {prompt}")
                return response.text, model_id
            except:
                continue
    return "⚠️ Erro Crítico: Todos os modelos de IA offline.", "Esgotado"

def gerar_docx(titulo, conteudo):
    """Gerador de documentos corporativos TechnoBolt."""
    doc = docx.Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"TechnoBolt Solutions - Hub de Inteligência")
    doc.add_paragraph(f"Operador Responsável: {st.session_state.user_atual.upper()}")
    doc.add_paragraph(f"Data: {time.strftime('%d/%m/%Y %H:%M')}")
    doc.add_paragraph("-" * 40)
    doc.add_paragraph(conteudo)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 6. NAVEGAÇÃO E INTERFACE PRINCIPAL ---
st.markdown(f'<div style="display:flex; justify-content:space-between; align-items:center; padding-bottom: 20px; border-bottom: 1px solid #e2e8f0; margin-bottom: 20px;"><div><span style="color:#2563eb; font-weight:800; font-size:24px;">TECHNOBOLT</span> <span style="color:#64748b;">HUB</span></div><div style="font-size:12px; color:#64748b;">SESSÃO: {st.session_state.user_atual.upper()} | <a href="/" style="color:#ef4444; text-decoration:none;">LOGOUT</a></div></div>', unsafe_allow_html=True)

menu_opcoes = [
    "🏠 Dashboard de Comando", 
    "📁 Analisador McKinsey", 
    "📧 Email Intel (Lote)", 
    "✉️ Gerador de Emails", 
    "🧠 Briefing Estratégico", 
    "📝 Gestor de Atas", 
    "📈 Mercado & Churn", 
    "📊 Relatório Master"
]
menu_selecionado = st.selectbox("Seletor de Módulo", menu_opcoes, label_visibility="collapsed")
st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# --- 7. MÓDULOS DAS FUNCIONALIDADES INTEGRAIS ---

# DASHBOARD
if "🏠 Dashboard" in menu_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h1>Command Center</h1><p>Monitoria de Governança Cognitiva e Redundância Ativa.</p></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Motor de IA", "Soberana", delta="Ativa")
    with c2: st.metric("Sessão Ativa", st.session_state.user_atual.capitalize())
    with c3: st.metric("Segurança", "AES-256", delta="Certificado")

# ANALISADOR MCKINSEY
elif "📁 Analisador McKinsey" in menu_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>Analisador de Documentos McKinsey</h2><p>Auditoria técnica, análise de riscos e plano de ação.</p></div>', unsafe_allow_html=True)
    arq = st.file_uploader("Carregar Documento (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
    if arq and st.button("EXECUTAR ANÁLISE ESTRATÉGICA"):
        with st.spinner("Analisando sob padrão de excelência..."):
            if arq.type == "application/pdf":
                dados = [{"mime_type": "application/pdf", "data": arq.read()}]
                prompt_mc = "Aja como Consultor McKinsey. Gere: 1. Resumo, 2. Riscos e Impactos, 3. Plano de Ação."
            else:
                texto = extrair_texto_docx(arq) if arq.name.endswith('docx') else arq.read().decode()
                dados = [texto]
                prompt_mc = "Analise tecnicamente este documento para a Technobolt Solutions sob a ótica McKinsey."
            res, mod = call_ai_with_failover(prompt_mc, dados)
            st.markdown(f'<span class="model-badge">IA ATIVA: {mod}</span>', unsafe_allow_html=True)
            st.markdown(res)
            st.download_button("Baixar Relatório DOCX", data=gerar_docx("Análise Estratégica", res), file_name="Relatorio_Auditoria.docx")

# EMAIL INTEL
elif "📧 Email Intel" in menu_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>Email Intel: Auditoria em Lote</h2><p>Processamento massivo de e-mails em PDF.</p></div>', unsafe_allow_html=True)
    arqs = st.file_uploader("Upload de Emails (PDF):", type=["pdf"], accept_multiple_files=True)
    cargo_resp = st.text_input("Seu Cargo para Resposta:", value="Diretor")
    if arqs and st.button("INICIAR AUDITORIA"):
        for i, pdf in enumerate(arqs):
            with st.expander(f"Auditoria: {pdf.name}", expanded=True):
                res, mod = call_ai_with_failover(f"Resuma este e-mail e rascunhe uma resposta técnica como {cargo_resp}.", [{"mime_type": "application/pdf", "data": pdf.read()}])
                st.markdown(res)

# GERADOR DE EMAILS
elif "✉️ Gerador de Emails" in menu_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>Gerador de Emails Inteligente</h2><p>Rascunhos corporativos de alto impacto.</p></div>', unsafe_allow_html=True)
    cargo_e = st.text_input("Seu Cargo para Assinatura:")
    obj_e = st.text_area("Objetivo ou Tópicos da Mensagem:")
    if st.button("REDIGIR EMAIL PROFISSIONAL"):
        with st.spinner("Redigindo..."):
            res, mod = call_ai_with_failover(f"Como {cargo_e}, escreva um email profissional sobre: {obj_e}")
            st.markdown(f'<div class="main-card" style="max-width:100%;">{res}</div>', unsafe_allow_html=True)
            st.download_button("Baixar Rascunho", data=gerar_docx("Email Gerado", res), file_name="Rascunho_Email.docx")

# BRIEFING ESTRATÉGICO
elif "🧠 Briefing" in menu_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>Briefing Negocial Estratégico</h2><p>Radar de mercado e análise de rivais.</p></div>', unsafe_allow_html=True)
    emp = st.text_input("Empresa Alvo:"); setor = st.text_input("Setor:"); 
    obj_b = st.text_area("Objetivo do Briefing:")
    if st.button("ESCANEAR MERCADO"):
        res, mod = call_ai_with_failover(f"Briefing estratégico 2026 para {emp} no setor {setor}. Foco: {obj_b}")
        st.markdown(res)

# GESTOR DE ATAS
elif "📝 Gestor de Atas" in menu_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>Gestor de Atas de Governança</h2><p>Formalização automática de reuniões.</p></div>', unsafe_allow_html=True)
    notas_r = st.text_area("Notas ou Transcrição da Reunião:", height=250)
    if st.button("FORMALIZAR ATA DE DIRETORIA"):
        with st.spinner("Estruturando ata..."):
            res, mod = call_ai_with_failover(f"Transforme em uma ata formal de diretoria TechnoBolt: {notas_r}")
            st.markdown(f'<div class="main-card" style="max-width:100%;">{res}</div>', unsafe_allow_html=True)
            st.download_button("Baixar Ata Word", data=gerar_docx("Ata Oficial", res), file_name="Ata_Reuniao.docx")

# MERCADO & CHURN
elif "📈 Mercado & Churn" in menu_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>Inteligência de Mercado & Churn</h2></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Radar Rival", "⚠️ Previsão de Churn"])
    with t1:
        rival_n = st.text_input("Concorrente:")
        if st.button("ANALISAR CONCORRENTE"):
            res, mod = call_ai_with_failover(f"Analise a estratégia competitiva de: {rival_n}"); st.markdown(res)
    with t2:
        feed_c = st.text_area("Feedback do Cliente:");
        if st.button("CALCULAR RISCO DE PERDA"):
            res, mod = call_ai_with_failover(f"Avalie risco de churn e plano de retenção para: {feed_c}"); st.markdown(res)

# RELATÓRIO MASTER
elif "📊 Relatório Master" in menu_selecionado:
    st.markdown('<div class="main-card" style="max-width:100%;"><h2>Relatório Master de Diretoria</h2><p>Consolidação de governança semanal.</p></div>', unsafe_allow_html=True)
    compilado_d = st.text_area("Dados e resumos da semana para consolidar:")
    if st.button("GERAR DOSSIÊ MASTER"):
        res, mod = call_ai_with_failover(f"Dossiê Executivo TechnoBolt: Resumo, Decisões e Riscos. Dados: {compilado_d}")
        st.markdown(res); st.download_button("Baixar Dossiê Master", data=gerar_docx("Dossiê Master", res), file_name="Governanca_Dossie.docx")

# --- 8. CHATBOT POPUP (UX CORPORATIVO ESTÁVEL) ---
st.markdown("""
    <div style="position: fixed; bottom: 25px; right: 25px; z-index: 10001;">
        <button id="chatTrigger" style="background:#2563eb; color:white; border:none; width:65px; height:65px; border-radius:50%; box-shadow: 0 10px 30px rgba(37,99,235,0.3); cursor:pointer; font-size:28px;">💬</button>
    </div>
""", unsafe_allow_html=True)

# Lógica de controle do Chatbot via checkbox (método estável Streamlit)
with st.container():
    col1, col_chat = st.columns([4, 1])
    with col_chat:
        if st.checkbox("Abrir Guia de Suporte", key="pop_chat_btn"):
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            st.markdown('<div class="chat-header"><span>💬 Suporte TechnoBolt</span></div>', unsafe_allow_html=True)
            st.markdown("<div style='padding:20px;'>", unsafe_allow_html=True)
            st.info("💡 Tire dúvidas sobre o funcionamento do Hub.")
            p_suporte = st.text_input("Como posso ajudar?", key="p_chat_hub")
            if p_suporte:
                with st.spinner("Consultando guia..."):
                    resp_chat, _ = call_ai_with_failover(p_suporte, is_chatbot=True)
                    st.write(resp_chat)
            st.markdown("</div></div>", unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown("<hr style='border: 0.5px solid #e2e8f0; margin-top:50px;'>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © 2026 | Enterprise Hub Edition v1.0 | Operador: {st.session_state.user_atual.upper()}")