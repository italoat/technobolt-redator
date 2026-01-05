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

# --- 2. CSS UX-ADVANCED & ZERO WHITE (ESTÉTICA CIBERNÉTICA AZUL) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

    /* 1. FUNDO AZUL ESCURO CIBERNÉTICO ABSOLUTO */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background: radial-gradient(circle at center, #0a192f 0%, #020617 100%) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #e2e8f0 !important;
    }

    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    * { color: #f8fafc !important; }

    /* 2. CARD DE LOGIN UX-ADVANCED CENTRALIZADO */
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

    /* 3. TÍTULO TECH COM GRADIENTE */
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

    /* 4. INPUTS MODERNOS (UX PREMIUM) */
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

    /* 5. FIX BOTÃO SEM LINHA PRETA ATRÁS DA FONTE */
    .stButton > button { 
        width: 100%; border-radius: 20px; height: 4.5em; font-weight: 700; 
        background: linear-gradient(90deg, #1d4ed8 0%, #3b82f6 100%) !important; 
        color: #ffffff !important; border: none !important;
        text-transform: uppercase; letter-spacing: 2px;
        transition: 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        display: flex; align-items: center; justify-content: center;
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

    /* 6. LISTA SUSPENSA E SELECTBOX DARK (CORREÇÃO DE MANCHA BRANCA) */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="popover"], 
    div[data-baseweb="popover"] > div,
    ul[role="listbox"], 
    [data-baseweb="listbox"] {
        background-color: #0f172a !important;
        color: white !important;
        border: 1px solid #1e3a8a !important;
    }

    /* 7. BADGE DE STATUS IA */
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
    st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
    col1, col_login, col3 = st.columns([1, 2, 1])
    
    with col_login:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("""
            <p style='color: #60a5fa; font-weight: 800; letter-spacing: 5px; margin-bottom: 5px;'>SISTEMA ATIVO</p>
            <h1 class='main-title'>TECHNOBOLT - HUB DE GOVERNANÇA COGNITIVA</h1>
            <p style='color: #94a3b8; font-size: 15px; margin-bottom: 50px; letter-spacing: 1px;'>IDENTIFIQUE-SE PARA CONEXÃO SEGURA</p>
        """, unsafe_allow_html=True)
        
        u_in = st.text_input("USUÁRIO IDENTIFICADOR", placeholder="Identidade do Operador")
        
        col_pwd, col_eye = st.columns([0.88, 0.12])
        with col_eye:
            st.markdown("<div style='height: 42px;'></div>", unsafe_allow_html=True)
            ver_senha = st.checkbox("👁️", help="Visualizar Senha")
        with col_pwd:
            p_in = st.text_input("CHAVE CRIPTOGRÁFICA", type="default" if ver_senha else "password", placeholder="Chave de Acesso")
        
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        if st.button("INICIAR CONEXÃO HUB"):
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
                st.error("⚠️ ACESSO NEGADO: Credenciais não autorizadas pelo protocolo.")
        
        st.markdown("<p style='color: #1e3a8a; font-size: 10px; margin-top: 45px; letter-spacing: 3px;'>PROTOCOLO DE SEGURANÇA MILITAR AES-256 ATIVO</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    tela_login()
    st.stop()

# --- 4. LÓGICA DE INTELIGÊNCIA COM FAILOVER (INTEGRAL E DETALHADA) ---
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

def call_ai_with_failover(prompt, content_list=None, is_chatbot=False):
    """Executa o prompt com instrução de sistema para remover saudações."""
    sys_instr = (
        "Você é o motor de inteligência da TechnoBolt Solutions. "
        "Sua saída deve ser estritamente profissional e técnica. "
        "PROIBIDO: Usar frases como 'Aqui está', 'Entendido', 'Como solicitado' ou saudações. "
        "ENTREGA: Responda diretamente com o conteúdo estruturado em Markdown."
    )
    
    if is_chatbot:
        sys_instr = (
            "Você é o Guia de Suporte TechnoBolt. Você só responde dúvidas sobre o sistema TechnoBolt IA Hub. "
            "Funcionalidades: Dashboard Inicial (Métricas de Status), Analisador de Documentos (Auditoria McKinsey de Contratos), "
            "Email Intel (Auditoria e Resposta em lote), Gerador de Email, Briefing Negocial (Radar estratégico), "
            "Analista de Atas, Inteligência Competitiva (Análise de rivais e Churn), Relatório Master (Dossiê semanal). "
            "Se perguntarem algo não relacionado ao sistema ou gestão corporativa, diga educadamente que não é uma função da ferramenta."
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
            # Fallback para modelos que não suportam system_instruction (versões legadas)
            try:
                model_fb = genai.GenerativeModel(model_id)
                full_prompt = f"{sys_instr}\n\nSOLICITAÇÃO: {prompt}"
                response = model_fb.generate_content([full_prompt] + content_list if content_list else full_prompt)
                return response.text, model_id
            except:
                continue
    return "⚠️ Cota esgotada em todos os modelos de redundância.", "Esgotado"

def gerar_docx(titulo, conteudo):
    doc = docx.Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"TechnoBolt Solutions - Relatório Gerado em: {time.strftime('%d/%m/%Y %H:%M')}")
    doc.add_paragraph(f"Operador Responsável: {st.session_state.user_atual.upper()}")
    doc.add_paragraph("-" * 30)
    doc.add_paragraph(conteudo)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 5. NAVEGAÇÃO SUPERIOR ---
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
    "📊 Relatório Master de Governança",
    "💬 Suporte & Guia TechnoBolt"
]
menu_selecionado = st.selectbox("Seletor de Módulo", menu_opcoes, label_visibility="collapsed")
st.markdown("<hr>", unsafe_allow_html=True)

# --- 6. TELAS DO HUB (CONTEÚDO INTEGRAL RESTAURADO) ---

# DASHBOARD
if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>Centro de Comando Corporativo</h1><p>Monitoria Cognitiva e Governança em Tempo Real</p></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Status da IA", "Soberana", delta="Failover Ativo")
    with c2: st.metric("Operador Autenticado", st.session_state.user_atual.capitalize())
    with c3: st.metric("Proteção de Dados", "AES-256", delta="Criptografado")
    st.info("O TechnoBolt IA Hub está pronto. Selecione um módulo técnico acima para processamento de dados.")

# CHATBOT DE SUPORTE (NOVO)
elif "💬 Suporte & Guia" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>💬 Suporte TechnoBolt</h1><p>Dúvidas sobre o funcionamento do ecossistema e funcionalidades.</p></div>', unsafe_allow_html=True)
    st.markdown("### 💡 Perguntas Frequentes:")
    cb1, cb2, cb3 = st.columns(3)
    with cb1:
        if st.button("Como funciona o Analisador?"): q_sug = "Como funciona o módulo Analisador de Documentos?"
    with cb2:
        if st.button("O que é o Relatório Master?"): q_sug = "O que é o Relatório Master de Governança?"
    with cb3:
        if st.button("O que é Soberania Digital?"): q_sug = "O que significa a Soberania e Redundância do sistema?"
    
    pergunta = st.chat_input("Pergunte sobre as funcionalidades da ferramenta...")
    if pergunta:
        with st.chat_message("user"): st.markdown(pergunta)
        with st.chat_message("assistant"):
            res, mod = call_ai_with_failover(pergunta, is_chatbot=True)
            st.markdown(res)

# EMAIL INTEL (AUDITORIA EM LOTE PDF)
elif "📧 Email Intel" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📧 Email Intel: Auditoria & Resposta</h1></div>', unsafe_allow_html=True)
    col_u, col_r = st.columns([1, 2])
    with col_u:
        arquivos = st.file_uploader("Anexe e-mails (PDF):", type=["pdf"], accept_multiple_files=True)
        cargo = st.text_input("Seu Cargo para Resposta:", placeholder="Ex: Diretor de Operações")
        tom = st.selectbox("Tom da Resposta:", ["Executivo/Direto", "Diplomático", "Cordial", "Firme"])
        btn_audit = st.button("🔍 INICIAR AUDITORIA EM LOTE")
    with col_r:
        if arquivos and btn_audit:
            for i, pdf in enumerate(arquivos):
                with st.expander(f"Auditoria: {pdf.name}", expanded=True):
                    with st.spinner(f"Analisando {pdf.name}..."):
                        pdf_data = [{"mime_type": "application/pdf", "data": pdf.read()}]
                        prompt_audit = f"Resuma este e-mail, identifique pontos de atenção e rascunhe uma resposta como {cargo} em tom {tom}."
                        res_texto, mod_ativo = call_ai_with_failover(prompt_audit, pdf_data)
                        st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod_ativo}</span>', unsafe_allow_html=True)
                        st.markdown(res_texto)
                        st.download_button(f"📩 Baixar Auditoria {i+1}", data=gerar_docx(f"Auditoria: {pdf.name}", res_texto), file_name=f"Auditoria_{pdf.name}.docx")

# ANALISADOR DE DOCUMENTOS (MCKINSEY)
elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos & Contratos</h1></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Upload (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
    if arquivo and st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
        with st.spinner("IA processando dados técnicos..."):
            if arquivo.type == "application/pdf":
                dados = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                prompt_doc = "Aja como Consultor McKinsey. Gere: Resumo Executivo, Impacto (Risco/Custo) e Plano de Ação.(Contudo o nome da sua consultoria é Technobolt)"
            else:
                texto_raw = extrair_texto_docx(arquivo) if arquivo.name.endswith('docx') else arquivo.read().decode()
                dados = [texto_raw]
                prompt_doc = "Analise o texto a seguir sob a ótica de negócios para a Technobolt Solutions:"
            res_doc, mod_doc = call_ai_with_failover(prompt_doc, dados)
            st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod_doc}</span>', unsafe_allow_html=True)
            st.markdown(res_doc)
            st.download_button("📄 Baixar Relatório", data=gerar_docx("Análise Estratégica", res_doc), file_name="Relatorio_TechnoBolt.docx")

# GERADOR DE EMAIL INDIVIDUAL
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email Inteligente</h1></div>', unsafe_allow_html=True)
    cargo_e = st.text_input("Seu Cargo:")
    obj_e = st.text_area("Objetivo da Mensagem:")
    formalidade = st.select_slider("Formalidade:", ["Casual", "Executivo", "Rígido"], value="Executivo")
    if st.button("🚀 GERAR COMUNICAÇÃO"):
        res, mod = call_ai_with_failover(f"Como {cargo_e}, escreva um email sobre {obj_e} em tom {formalidade}.")
        st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod}</span>', unsafe_allow_html=True)
        st.text_area("Rascunho:", res, height=400)
        st.download_button("✉️ Baixar Rascunho", data=gerar_docx("Rascunho de Email", res), file_name="Rascunho_Email.docx")

# BRIEFING NEGOCIAL ESTRATÉGICO
elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Negocial Estratégico</h1></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        empresa_alvo = st.text_input("Empresa Alvo:", placeholder="Ex: Petrobras, Google, etc.")
    with col2:
        setor_atuacao = st.text_input("Setor:", placeholder="Ex: Energia, Tecnologia...")
    objetivo = st.text_area("Objetivo da Análise:", placeholder="Ex: Avaliar potencial de fusão ou riscos de mercado para 2026.")
    if st.button("⚡ ESCANEAR MERCADO"):
        if empresa_alvo:
            with st.spinner(f"IA Nexus gerando radar para {empresa_alvo}..."):
                prompt_b = f"Gere um briefing estratégico 2026 para a empresa {empresa_alvo} no setor {setor_atuacao}. Foque em: {objetivo}. Traga: Cenário Macro, Movimentação de Rivais e 3 Recomendações Críticas."
                res, mod = call_ai_with_failover(prompt_b)
                st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod}</span>', unsafe_allow_html=True)
                st.markdown(res)
                st.download_button("🧠 Baixar Briefing", data=gerar_docx(f"Briefing: {empresa_alvo}", res), file_name=f"Briefing_{empresa_alvo}.docx")
        else:
            st.warning("Por favor, informe a empresa alvo.")

# ANALISTA DE ATAS
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas de Governança</h1></div>', unsafe_allow_html=True)
    notas = st.text_area("Notas da reunião (Transcrições ou tópicos):", height=300)
    if st.button("📝 FORMALIZAR ATA"):
        res, mod = call_ai_with_failover(f"Transforme em ata formal de diretoria: {notas}")
        st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod}</span>', unsafe_allow_html=True)
        st.markdown(res)
        st.download_button("📝 Baixar Ata Oficial", data=gerar_docx("Ata de Reunião", res), file_name="Ata_Governança.docx")

# INTELIGÊNCIA COMPETITIVA & CHURN
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência Competitiva & Churn</h1></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Radar Rival", "⚠️ Radar de Churn"])
    with t1:
        rival = st.text_input("Nome do Rival:")
        if st.button("📡 ANALISAR RIVAL"):
            res, mod = call_ai_with_failover(f"Analise a estratégia atual da empresa {rival}.")
            st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod}</span>', unsafe_allow_html=True)
            st.markdown(res)
            st.download_button("📈 Baixar Radar", data=gerar_docx(f"Radar Competitivo: {rival}", res), file_name=f"Radar_{rival}.docx")
    with t2:
        feed = st.text_area("Feedback ou Comportamento do cliente:")
        if st.button("🧠 PREVER RISCO"):
            res, mod = call_ai_with_failover(f"Avalie o risco de churn e dê um plano de retenção para: {feed}")
            st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod}</span>', unsafe_allow_html=True)
            st.markdown(res)
            st.download_button("⚠️ Baixar Análise de Risco", data=gerar_docx("Análise de Risco", res), file_name="Analise_Churn.docx")

# RELATÓRIO MASTER DE GOVERNANÇA
elif "📊 Relatório Master" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📊 Relatório Master de Governança</h1></div>', unsafe_allow_html=True)
    compilado = st.text_area("Cole aqui todos os resumos e notas da semana para consolidação:", height=400)
    if st.button("🚀 GERAR DOSSIÊ SEMANAL"):
        if compilado:
            with st.spinner("IA TechnoBolt estruturando governança semanal..."):
                prompt_master = f"Aja como um Chief of Staff da TechnoBolt Solutions. Organize os seguintes dados em um Relatório Semanal de Governança Profissional estruturado em: 1. RESUMO EXECUTIVO, 2. DECISÕES TOMADAS, 3. RISCOS E ALERTAS e 4. PRÓXIMOS PASSOS. Dados: {compilado}"
                res_master, mod_master = call_ai_with_failover(prompt_master)
                st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod_master}</span>', unsafe_allow_html=True)
                st.markdown(res_master)
                st.download_button("📊 Baixar Relatório Master", data=gerar_docx("Relatório Semanal de Governança", res_master), file_name="Governanca_Semanal.docx")
        else:
            st.warning("Insira o conteúdo para consolidar.")

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © 2026 | Operador: {st.session_state.user_atual.upper()} | Master Resilience Edition v1.3")