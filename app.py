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

# --- 2. CSS ULTRA-PREMIUM (DARK MODE ABSOLUTO E BLINDAGEM VISUAL) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');

    /* 1. FUNDO PRETO GLOBAL ABSOLUTO */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
    .stApp, [data-testid="stMain"], [data-testid="stVerticalBlock"],
    [data-testid="stMarkdownContainer"], .main, [data-testid="stBlock"] {
        background-color: #05070a !important;
        font-family: 'Inter', sans-serif !important;
        color: #ffffff !important;
    }

    /* 2. REMOÇÃO DE ELEMENTOS NATIVOS */
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* 3. FORÇA FONTES BRANCAS EM TUDO */
    * { 
        color: #f8fafc !important; 
        -webkit-text-fill-color: #f8fafc !important;
    }

    /* 4. TÍTULO CORPORATIVO COM GRADIENTE */
    .main-title { 
        font-size: 48px; font-weight: 900; text-align: center; 
        background: linear-gradient(to right, #60a5fa, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent !important;
        letter-spacing: -2px; margin-bottom: 5px;
    }

    .product-header { 
        background: rgba(30, 41, 59, 0.4); 
        backdrop-filter: blur(12px);
        padding: 40px; border-radius: 24px; margin-bottom: 35px; 
        text-align: center; border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 5. CORREÇÃO "NUCLEAR" DA BARRA DE SERVIÇOS (SELECTBOX) E POPOVER */
    /* Fundo da barra fechada */
    div[data-baseweb="select"] > div {
        background-color: #161b22 !important;
        border-radius: 12px !important;
    }

    /* Fundo da barra e da lista flutuante aberta */
    div[data-baseweb="select"], 
    div[data-baseweb="popover"], 
    div[data-baseweb="popover"] > div,
    ul[role="listbox"], 
    [data-baseweb="listbox"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
    }
    
    /* Itens individuais da lista suspensa */
    li[role="option"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        transition: 0.2s;
    }
    
    li[role="option"]:hover, li[aria-selected="true"] {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }

    /* 6. INPUTS E TEXTAREAS (CINZA ESCURO) */
    .stTextInput input, .stTextArea textarea {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* 7. BOTÃO "BROWSE FILES" E ÁREA DE UPLOAD */
    [data-testid="stFileUploader"] section {
        background-color: #161b22 !important;
        border: 2px dashed #3b82f6 !important;
        border-radius: 15px !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        padding: 10px 25px !important;
    }

  /* 8. BOTÕES EXECUTIVOS - CORREÇÃO DEFINITIVA DA BARRA INTERNA */
    .stButton > button { 
        width: 100%; 
        border-radius: 12px; 
        height: 4em; 
        font-weight: 700; 
        background-color: #262c36 !important; 
        color: #ffffff !important; 
        border: 1px solid #30363d !important;
        outline: none !important;
        box-shadow: none !important; 
        text-transform: uppercase;
        letter-spacing: 1.5px;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* REMOVE A FAIXA PRETA INTERNA (CONTAINER DE TEXTO DO STREAMLIT) */
    .stButton > button div[data-testid="stMarkdownContainer"], 
    .stButton > button p {
        background-color: transparent !important; /* Torna o fundo do texto invisível */
        background: none !important;
        box-shadow: none !important;
        text-shadow: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .stButton > button:hover {
        background-color: #30363d !important;
        border-color: #60a5fa !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
    }

    .stButton > button:focus, .stButton > button:active {
        background-color: #161b22 !important;
        border-color: #3b82f6 !important;
    }
    /* 9. SLIDER E TABS */
    .stSlider label, .stSlider span { color: #ffffff !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: 700; }

    hr { border: 0.5px solid rgba(255, 255, 255, 0.1) !important; margin: 40px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE INTELIGÊNCIA COM FAILOVER (HIERARQUIA DE MODELOS) ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Lista prioritária baseada na sua chave API
MODEL_LIST = [
    "models/gemini-3-flash-preview",    # Primário (Alta Performance)
    "models/gemini-2.5-flash",          # Secundário (Estabilidade)
    "models/gemini-2.0-flash",          # Terciário (Velocidade)
    "models/gemini-2.0-flash-lite",     # Segurança (Cota Máxima)
    "models/gemini-flash-latest"        # Última Instância
]

def extrair_texto_docx(arquivo_docx):
    doc = docx.Document(arquivo_docx)
    return "\n".join([p.text for p in doc.paragraphs])

def call_ai_with_failover(prompt, content_list=None):
    """Executa o prompt tentando a lista de modelos em cascata."""
    for model_id in MODEL_LIST:
        try:
            model = genai.GenerativeModel(model_id)
            if content_list:
                response = model.generate_content([prompt] + content_list)
            else:
                response = model.generate_content(prompt)
            return response.text, model_id
        except Exception as e:
            if "429" in str(e): # Se erro for cota excedida, pula para o próximo
                continue
            return f"Erro técnico no motor {model_id}: {e}", "Falha"
    return "⚠️ Cota esgotada em todos os modelos Flash da sua API Key.", "Esgotado"

# --- ADIÇÃO: FUNÇÃO DE EXPORTAÇÃO ---
def gerar_docx(titulo, conteudo):
    doc = docx.Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"TechnoBolt IA - Relatório Gerado em: {time.strftime('%d/%m/%Y %H:%M')}")
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
    "📈 Inteligência Competitiva & Churn"
]
menu_selecionado = st.selectbox("Navegação", menu_opcoes, label_visibility="collapsed")
st.markdown("<hr>", unsafe_allow_html=True)

# --- 5. TELAS DO HUB ---

# DASHBOARD
if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown("### Centro de Comando Corporativo")
    st.write("Hub unificado de inteligência para alta gestão com redundância de modelos.")
    st.info("Selecione um módulo acima para iniciar.")

# NOVO MÓDULO: EMAIL INTEL (AUDITORIA EM LOTE PDF)
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
                        st.markdown(f'<span class="model-badge">Processado por: {mod_ativo}</span>', unsafe_allow_html=True)
                        st.markdown(res_texto)
                        st.download_button(f"📩 Baixar Auditoria {i+1}", data=gerar_docx(f"Auditoria: {pdf.name}", res_texto), file_name=f"Auditoria_{pdf.name}.docx")

# ANALISADOR DE DOCUMENTOS
elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos</h1></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Upload (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
    if arquivo and st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
        with st.spinner("IA processando dados técnicos..."):
            if arquivo.type == "application/pdf":
                dados = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                prompt_doc = "Aja como Consultor McKinsey. Gere: Resumo Executivo, Impacto (Risco/Custo) e Plano de Ação.(Contudo o nome da sua consultoria é Technobolt)"
            else:
                texto_raw = extrair_texto_docx(arquivo) if arquivo.name.endswith('docx') else arquivo.read().decode()
                dados = [texto_raw]
                prompt_doc = "Analise o texto a seguir sob a ótica de negócios:"
            
            res_doc, mod_doc = call_ai_with_failover(prompt_doc, dados)
            st.markdown(f'<span class="model-badge">Motor Ativo: {mod_doc}</span>', unsafe_allow_html=True)
            st.markdown(res_doc)
            st.download_button("📄 Baixar Relatório", data=gerar_docx("Análise Estratégica", res_doc), file_name="Relatorio.docx")

# GERADOR DE EMAIL INDIVIDUAL
elif "✉️ Gerador de Email" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>✉️ Gerador de Email</h1></div>', unsafe_allow_html=True)
    cargo_e = st.text_input("Seu Cargo:")
    obj_e = st.text_area("Objetivo da Mensagem:")
    formalidade = st.select_slider("Formalidade:", ["Casual", "Executivo", "Rígido"], value="Executivo")
    if st.button("🚀 GERAR COMUNICAÇÃO"):
        res, mod = call_ai_with_failover(f"Como {cargo_e}, escreva um email sobre {obj_e} em tom {formalidade}.")
        st.markdown(f'<span class="model-badge">Motor: {mod}</span>', unsafe_allow_html=True)
        st.text_area("Rascunho:", res, height=400)
        st.download_button("✉️ Baixar Rascunho", data=gerar_docx("Rascunho de Email", res), file_name="Rascunho_Email.docx")
        
# TELA: BRIEFING NEGOCIAL (RESTAURADA E COMPLETA)
elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown("### 🧠 Briefing Negocial Estratégico")
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
                st.markdown(f'<span class="model-badge">Motor: {mod}</span>', unsafe_allow_html=True)
                st.markdown(res)
                st.download_button("🧠 Baixar Briefing", data=gerar_docx(f"Briefing: {empresa_alvo}", res), file_name=f"Briefing_{empresa_alvo}.docx")
        else:
            st.warning("Por favor, informe a empresa alvo.")

# ANALISTA DE ATAS
elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas</h1></div>', unsafe_allow_html=True)
    notas = st.text_area("Notas da reunião:", height=300)
    if st.button("📝 FORMALIZAR ATA"):
        res, mod = call_ai_with_failover(f"Transforme em ata formal de diretoria: {notas}")
        st.markdown(f'<span class="model-badge">Motor: {mod}</span>', unsafe_allow_html=True)
        st.markdown(res)
        st.download_button("📝 Baixar Ata Oficial", data=gerar_docx("Ata de Reunião", res), file_name="Ata_Governança.docx")

# INTELIGÊNCIA COMPETITIVA
elif "📈 Inteligência Competitiva" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📈 Inteligência & Churn</h1></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔍 Radar Rival", "⚠️ Churn"])
    with t1:
        rival = st.text_input("Rival:")
        if st.button("📡 ANALISAR"):
            res, mod = call_ai_with_failover(f"Analise a estratégia da empresa {rival}.")
            st.markdown(f'<span class="model-badge">Motor: {mod}</span>', unsafe_allow_html=True)
            st.markdown(res)
            st.download_button("📈 Baixar Radar", data=gerar_docx(f"Radar Competitivo: {rival}", res), file_name=f"Radar_{rival}.docx")
    with t2:
        feed = st.text_area("Feedback do cliente:")
        if st.button("🧠 PREVER RISCO"):
            res, mod = call_ai_with_failover(f"Risco de churn para: {feed}")
            st.markdown(f'<span class="model-badge">Motor: {mod}</span>', unsafe_allow_html=True)
            st.markdown(res)
            st.download_button("⚠️ Baixar Análise de Churn", data=gerar_docx("Análise de Risco", res), file_name="Analise_Churn.docx")

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Master Resilience Edition v10.1")