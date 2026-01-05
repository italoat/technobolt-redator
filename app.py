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

# --- 2. CSS ULTRA-PREMIUM (DARK MODE ASSISTANT & GLASSMORPHISM) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

    /* 1. FUNDO PRETO GLOBAL ABSOLUTO E FONTE MODERNA */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
    .stApp, [data-testid="stMain"], [data-testid="stVerticalBlock"],
    [data-testid="stMarkdownContainer"], .main, [data-testid="stBlock"] {
        background-color: #05070a !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #e2e8f0 !important;
    }

    /* 2. REMOÇÃO DE ELEMENTOS NATIVOS */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* 3. FORÇA FONTES CLARAS EM TUDO */
    * { 
        color: #f8fafc !important; 
    }

    /* 4. TÍTULO CORPORATIVO COM GRADIENTE COBALTO & OURO */
    .main-title { 
        font-size: 52px; font-weight: 800; text-align: center; 
        background: linear-gradient(135deg, #3b82f6, #6366f1, #d4af37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent !important;
        letter-spacing: -3px; margin-bottom: 5px;
        padding: 20px 0;
    }

    /* 5. HEADER COM EFEITO VIDRO (GLASSMORPHISM) */
    .product-header { 
        background: rgba(15, 23, 42, 0.6); 
        backdrop-filter: blur(15px);
        padding: 45px; border-radius: 28px; margin-bottom: 35px; 
        text-align: center; border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    /* 6. CORREÇÃO DA BARRA DE SERVIÇOS (SELECTBOX) - DARK AZUL */
    div[data-baseweb="select"] > div {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 14px !important;
    }

    div[data-baseweb="popover"], div[data-baseweb="popover"] > div,
    ul[role="listbox"], [data-baseweb="listbox"] {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
    }
    
    li[role="option"] {
        background-color: #0f172a !important;
        transition: 0.2s;
    }
    
    li[role="option"]:hover {
        background-color: #1e3a8a !important;
    }

    /* 7. INPUTS E TEXTAREAS (CINZA ESPACIAL) */
    .stTextInput input, .stTextArea textarea {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #1e293b !important;
        border-radius: 14px !important;
        padding: 15px !important;
    }

    /* 8. UPLOAD AREA (ESTILO TECH) */
    [data-testid="stFileUploader"] section {
        background-color: rgba(30, 41, 59, 0.2) !important;
        border: 2px dashed #1e3a8a !important;
        border-radius: 20px !important;
    }

    /* 9. BOTÕES EXECUTIVOS (GRADIENTE & ELEVAÇÃO) */
    .stButton > button { 
        width: 100%; 
        border-radius: 14px; 
        height: 4em; 
        font-weight: 700; 
        background: linear-gradient(135deg, #1e3a8a 0%, #0ea5e9 100%) !important; 
        color: #ffffff !important; 
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4) !important;
        filter: brightness(1.1);
    }

    /* REMOVE FUNDOS INTERNOS DO STREAMLIT NOS BOTÕES */
    .stButton > button div[data-testid="stMarkdownContainer"], 
    .stButton > button p {
        background: none !important;
        margin: 0 !important;
    }

    /* 10. BADGES DE STATUS (VERDE/DOURADO) */
    .model-badge {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981 !important;
        padding: 5px 15px;
        border-radius: 30px;
        border: 1px solid rgba(16, 185, 129, 0.5);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    /* 11. TABS E SLIDERS */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: 700; border-radius: 8px; }
    .stSlider label, .stSlider span { color: #ffffff !important; }

    hr { border: 0.5px solid rgba(255, 255, 255, 0.05) !important; margin: 40px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE INTELIGÊNCIA COM FAILOVER (HIERARQUIA DE MODELOS) ---
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
    """Executa o prompt com instrução de sistema para remover saudações."""
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
    return "⚠️ Cota esgotada.", "Esgotado"

def gerar_docx(titulo, conteudo):
    doc = docx.Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"TechnoBolt Solutions - Relatório Gerado em: {time.strftime('%d/%m/%Y %H:%M')}")
    doc.add_paragraph("-" * 30)
    doc.add_paragraph(conteudo)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 4. NAVEGAÇÃO SUPERIOR ---
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
menu_selecionado = st.selectbox("Navegação", menu_opcoes, label_visibility="collapsed")
st.markdown("<hr>", unsafe_allow_html=True)

# --- 5. TELAS DO HUB ---

# DASHBOARD
if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>Centro de Comando Corporativo</h1><p>Inteligência de Governança com Redundância Ativa</p></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Soberania", "Ativa", delta="Failover OK")
    with c2: st.metric("Processamento", "Neural", delta="Fast")
    with c3: st.metric("Segurança", "AES-256", delta="Protegido")
    st.info("Selecione um módulo de governança no menu superior para iniciar.")

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

# ANALISADOR DE DOCUMENTOS
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
                prompt_doc = "Analise o texto a seguir sob a ótica de negócios para a Technobolt:"
            
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
        
# BRIEFING NEGOCIAL
elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>🧠 Briefing Negocial Estratégico</h1></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        empresa_alvo = st.text_input("Empresa Alvo:", placeholder="Ex: Petrobras, Google, etc.")
    with col2:
        setor_atuacao = st.text_input("Setor:", placeholder="Ex: Energia, Tecnologia...")
    
    objetivo = st.text_area("Objetivo da Análise:", placeholder="Ex: Avaliar potencial de fusão...")
    
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

# INTELIGÊNCIA COMPETITIVA
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

# RELATÓRIO MASTER
elif "📊 Relatório Master" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📊 Relatório Master de Governança</h1></div>', unsafe_allow_html=True)
    st.write("Consolide todas as análises, e-mails e reuniões da semana em um dossiê executivo.")
    compilado = st.text_area("Cole aqui os resumos e notas da semana:", height=400)
    if st.button("🚀 GERAR DOSSIÊ SEMANAL"):
        if compilado:
            with st.spinner("IA TechnoBolt estruturando governança semanal..."):
                prompt_master = f"Aja como um Chief of Staff da TechnoBolt Solutions. Organize os seguintes dados em um Relatório Semanal de Governança Profissional estruturado em: 1. RESUMO EXECUTIVO, 2. DECISÕES TOMADAS, 3. RISCOS E ALERTAS e 4. PRÓXIMOS PASSOS. Dados: {compilado}"
                res_master, mod_master = call_ai_with_failover(prompt_master)
                st.markdown(f'<span class="model-badge">SISTEMA ATIVO: {mod_master}</span>', unsafe_allow_html=True)
                st.markdown(res_master)
                st.download_button("📊 Baixar Relatório Master", data=gerar_docx("Relatório Semanal", res_master), file_name="Governanca_Semanal.docx")

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Master Resilience Edition v10.1 - Soberania em Inteligência Artificial")