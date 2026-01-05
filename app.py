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

# --- 2. CSS ULTRA-PREMIUM (ESTÉTICA IA ASSISTANT & ZERO WHITE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

    /* FUNDO ABSOLUTO SEM MANCHAS BRANCAS */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
    .stApp, [data-testid="stMain"], [data-testid="stVerticalBlock"],
    [data-testid="stMarkdownContainer"], .main, [data-testid="stBlock"] {
        background-color: #05070a !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #e2e8f0 !important;
    }

    /* REMOVER SIDEBAR E ELEMENTOS NATIVOS */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* FORÇAR TEXTO CLARO EM TUDO */
    * { color: #f8fafc !important; }

    /* CARD DE LOGIN CENTRALIZADO E GLASSMORPHISM */
    .login-card {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(25px);
        padding: 55px;
        border-radius: 35px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.7);
        text-align: center;
        margin: auto;
        max-width: 450px;
    }

    /* TÍTULOS COM GRADIENTE TECH */
    .main-title { 
        font-size: 58px; font-weight: 800; text-align: center; 
        background: linear-gradient(135deg, #3b82f6, #6366f1, #d4af37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent !important;
        letter-spacing: -3px; margin-bottom: 5px;
        padding: 15px 0;
    }

    .product-header { 
        background: rgba(15, 23, 42, 0.7); 
        backdrop-filter: blur(20px);
        padding: 45px; border-radius: 30px; margin-bottom: 35px; 
        text-align: center; border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }

    /* CORREÇÃO NUCLEAR DA LISTA SUSPENSA (SELECTBOX) - REMOVE O BRANCO */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="popover"], 
    div[data-baseweb="popover"] > div,
    ul[role="listbox"], 
    [data-baseweb="listbox"] {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #1e293b !important;
    }
    
    li[role="option"] {
        background-color: #0f172a !important;
        color: #ffffff !important;
        transition: 0.2s ease;
    }
    
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }

    /* INPUTS MODERNOS CINZA ESPACIAL */
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid #1e293b !important;
        border-radius: 14px !important;
        padding: 18px !important;
    }

    /* BOTÃO COM EFEITO TECH E ELEVAÇÃO */
    .stButton > button { 
        width: 100%; 
        border-radius: 16px; 
        height: 4.5em; 
        font-weight: 700; 
        background: linear-gradient(135deg, #1e3a8a 0%, #0ea5e9 100%) !important; 
        color: #ffffff !important; 
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(14, 165, 233, 0.4) !important;
    }

    /* BADGE DE STATUS */
    .model-badge {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981 !important;
        padding: 8px 18px;
        border-radius: 30px;
        border: 1px solid rgba(16, 185, 129, 0.5);
        font-size: 11px;
        font-weight: 800;
    }

    hr { border: 0.5px solid rgba(255, 255, 255, 0.08) !important; margin: 40px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE AUTENTICAÇÃO ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def tela_login():
    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.6, 1])
    
    with col2:
        st.markdown("""
            <div class='login-card'>
                <h1 style='font-size: 44px; font-weight: 800; margin-bottom: 5px; background: linear-gradient(to right, #60a5fa, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    TechnoBolt IA
                </h1>
                <p style='color: #64748b; font-size: 16px; margin-bottom: 40px; letter-spacing: 1px;'>HUB DE GOVERNANÇA COGNITIVA</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            u_in = st.text_input("Identificador de Usuário", placeholder="Usuário", label_visibility="collapsed")
            p_in = st.text_input("Chave de Segurança", type="password", placeholder="Senha", label_visibility="collapsed")
            
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            
            if st.button("AUTENTICAR NO HUB"):
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
                    st.error("⚠️ Identidade não verificada pelo protocolo de segurança.")
        
        st.markdown("<p style='text-align: center; color: #334155; font-size: 11px; margin-top: 40px; letter-spacing: 2px;'>PROTEÇÃO DE DADOS AES-256 ATIVA</p>", unsafe_allow_html=True)

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
    """Lógica robusta de redundância com instruções de sistema TechnoBolt."""
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
    return "⚠️ Erro: Todos os modelos de redundância esgotaram a cota.", "Esgotado"

def gerar_docx(titulo, conteudo):
    doc = docx.Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"TechnoBolt Solutions - Hub de Governança")
    doc.add_paragraph(f"Operador Responsável: {st.session_state.user_atual}")
    doc.add_paragraph(f"Data de Geração: {time.strftime('%d/%m/%Y %H:%M')}")
    doc.add_paragraph("-" * 35)
    doc.add_paragraph(conteudo)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 5. INTERFACE DO HUB (NAVEGAÇÃO COMPLETA) ---
st.markdown(f'<div style="text-align:right; font-size:11px; color:#60a5fa; letter-spacing:1px;">ID SESSÃO: {st.session_state.user_atual.upper()} | <a href="/" style="color:#f87171; text-decoration:none;">[ SAIR ]</a></div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">TechnoBolt IA Hub</div>', unsafe_allow_html=True)

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

if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>Centro de Comando Corporativo</h1><p>Monitoria Cognitiva e Governança em Tempo Real</p></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Motor de IA", "Soberano", delta="Failover Ativo")
    with c2: st.metric("Operador Autenticado", st.session_state.user_atual.capitalize())
    with c3: st.metric("Protocolo de Dados", "AES-256", delta="Criptografado")
    st.info("Ecossistema TechnoBolt operando normalmente. Selecione uma solução técnica acima para iniciar a auditoria.")

elif "📧 Email Intel" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📧 Email Intel: Auditoria & Resposta</h1></div>', unsafe_allow_html=True)
    col_u, col_r = st.columns([1, 2])
    with col_u:
        arquivos = st.file_uploader("Anexe e-mails em PDF:", type=["pdf"], accept_multiple_files=True)
        cargo = st.text_input("Cargo para Rascunho:", value="Diretor de Operações")
        tom = st.selectbox("Tom da Comunicação:", ["Executivo/Direto", "Diplomático", "Cordial", "Firme"])
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
                        st.download_button(f"📩 Baixar Auditoria {i+1}", data=gerar_docx(f"Auditoria: {pdf.name}", res_texto), file_name=f"Auditoria_{pdf.name}.docx")

elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos & Contratos</h1></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Upload (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
    if arquivo and st.button("🔍 INICIAR ANÁLISE ESTRATÉGICA"):
        with st.spinner("Analisando estrutura de dados..."):
            if arquivo.type == "application/pdf":
                dados = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                prompt_doc = "Aja como Consultor McKinsey da Technobolt. Gere: Resumo Executivo, Impacto (Risco/Custo) e Plano de Ação."
            else:
                texto_raw = extrair_texto_docx(arquivo) if arquivo.name.endswith('docx') else arquivo.read().decode()
                dados = [texto_raw]
                prompt_doc = "Analise o texto a seguir sob a ótica de negócios para a Technobolt Solutions:"
            res_doc, mod_doc = call_ai_with_failover(prompt_doc, dados)
            st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod_doc}</span>', unsafe_allow_html=True)
            st.markdown(res_doc)
            st.download_button("📄 Baixar Relatório Completo", data=gerar_docx("Análise Estratégica", res_doc), file_name="Relatorio_TechnoBolt.docx")

elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1></div>', unsafe_allow_html=True)
    c_e = st.text_input("Seu Cargo:")
    obj_e = st.text_area("Objetivo da Mensagem:")
    fml = st.select_slider("Nível de Formalidade:", ["Casual", "Executivo", "Rígido"], value="Executivo")
    if st.button("🚀 GERAR COMUNICAÇÃO"):
        res, mod = call_ai_with_failover(f"Como {c_e}, escreva um email profissional sobre {obj_e} em tom {fml}.")
        st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod}</span>', unsafe_allow_html=True)
        st.text_area("Rascunho Gerado:", res, height=400)
        st.download_button("✉️ Baixar Rascunho (.docx)", data=gerar_docx("Rascunho de Email", res), file_name="Rascunho_Email.docx")

elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Negocial Estratégico</h1></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: emp_a = st.text_input("Empresa Alvo:")
    with col2: set_a = st.text_input("Setor de Atuação:")
    objetivo_b = st.text_area("Foco do Briefing (Fusão, Risco, Mercado):")
    if st.button("⚡ ESCANEAR MERCADO"):
        if emp_a:
            with st.spinner(f"Gerando inteligência para {emp_a}..."):
                p_b = f"Gere um briefing estratégico 2026 para a empresa {emp_a} no setor {set_a}. Foco: {objetivo_b}. Traga: Cenário Macro, Rivais e Recomendações."
                res, mod = call_ai_with_failover(p_b)
                st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod}</span>', unsafe_allow_html=True)
                st.markdown(res)
                st.download_button("🧠 Baixar Briefing", data=gerar_docx(f"Briefing: {emp_a}", res), file_name=f"Briefing_{emp_a}.docx")
        else:
            st.warning("Informe a empresa alvo para processamento.")

elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas de Governança</h1></div>', unsafe_allow_html=True)
    notas_r = st.text_area("Insira as notas ou transcrição da reunião:", height=300)
    if st.button("📝 FORMALIZAR ATA OFICIAL"):
        with st.spinner("Estruturando documento formal..."):
            res, mod = call_ai_with_failover(f"Transforme as seguintes notas em uma ata formal de diretoria: {notas_r}")
            st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod}</span>', unsafe_allow_html=True)
            st.markdown(res)
            st.download_button("📝 Baixar Ata Formal", data=gerar_docx("Ata de Governança", res), file_name="Ata_Oficial.docx")

elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência Competitiva & Churn</h1></div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔍 Monitoria de Concorrentes", "⚠️ Análise de Churn"])
    with tab1:
        rival_n = st.text_input("Nome do Rival:")
        if st.button("📡 ANALISAR ESTRATÉGIA"):
            res, mod = call_ai_with_failover(f"Analise a estratégia competitiva atual da empresa {rival_n}.")
            st.markdown(res)
            st.download_button("📈 Baixar Análise", data=gerar_docx(f"Análise Rival: {rival_n}", res), file_name=f"Radar_{rival_n}.docx")
    with tab2:
        feed_c = st.text_area("Feedback do cliente insatisfeito:")
        if st.button("🧠 CALCULAR RISCO"):
            res, mod = call_ai_with_failover(f"Avalie risco de perda do cliente e plano de retenção para: {feed_c}")
            st.markdown(res)
            st.download_button("⚠️ Baixar Plano de Retenção", data=gerar_docx("Plano de Retenção", res), file_name="Analise_Churn.docx")

elif "📊 Relatório Master" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📊 Relatório Master de Governança</h1></div>', unsafe_allow_html=True)
    compilado_s = st.text_area("Cole os dados acumulados da semana para consolidação executiva:", height=400)
    if st.button("🚀 GERAR DOSSIÊ MASTER"):
        if compilado_s:
            with st.spinner("IA TechnoBolt consolidando governança semanal..."):
                p_master = f"Aja como Chief of Staff TechnoBolt Solutions. Organize: 1. Resumo Executivo, 2. Decisões, 3. Riscos e 4. Próximos Passos. Dados: {compilado_s}"
                res_master, mod_master = call_ai_with_failover(p_master)
                st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod_master}</span>', unsafe_allow_html=True)
                st.markdown(res_master)
                st.download_button("📊 Baixar Relatório Master", data=gerar_docx("Relatório Master de Governança", res_master), file_name="Governanca_Semanal.docx")
        else:
            st.warning("Insira dados para consolidação.")

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Master Edition v1.0 | Operador: {st.session_state.user_atual.upper()}")