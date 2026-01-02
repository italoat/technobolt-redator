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

# --- 2. CSS ULTRA-PREMIUM (ESTRUTURA ORIGINAL SOLICITADA) ---
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

    /* 5. CORREÇÃO DA BARRA DE SERVIÇOS (SELECTBOX) E POPOVER */
    div[data-baseweb="select"] > div {
        background-color: #161b22 !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"], 
    div[data-baseweb="popover"], 
    div[data-baseweb="popover"] > div,
    ul[role="listbox"], 
    [data-baseweb="listbox"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
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

    /* 8. BOTÕES EXECUTIVOS - OBSIDIAN ANTRACITE EDITION (ORIGINAL) */
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
        text-shadow: none !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        transition: all 0.3s ease;
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
        box-shadow: none !important;
    }

    /* 9. SLIDER E TABS */
    .stSlider label, .stSlider span { color: #ffffff !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: 700; }

    hr { border: 0.5px solid rgba(255, 255, 255, 0.1) !important; margin: 40px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE INTELIGÊNCIA COM FAILOVER E EXPORTAÇÃO ---
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

MODEL_LIST = [
    "models/gemini-3-flash-preview", "models/gemini-2.5-flash", 
    "models/gemini-2.0-flash", "models/gemini-2.0-flash-lite", "models/gemini-flash-latest"
]

def extrair_texto_docx(arquivo_docx):
    doc = docx.Document(arquivo_docx)
    return "\n".join([p.text for p in doc.paragraphs])

def call_ai_with_failover(prompt, content_list=None):
    for model_id in MODEL_LIST:
        try:
            model = genai.GenerativeModel(model_id)
            response = model.generate_content([prompt] + content_list if content_list else prompt)
            return response.text, model_id
        except Exception as e:
            if "429" in str(e): continue
            return f"Erro técnico no motor {model_id}: {e}", "Falha"
    return "⚠️ Cota esgotada.", "Esgotado"

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

if "🏠 Dashboard Inicial" in menu_selecionado:
    st.markdown("### Centro de Comando Corporativo")
    st.write("Hub unificado de inteligência para alta gestão com redundância de modelos.")
    st.info("Selecione um módulo acima para iniciar as análises de monitoria.")

elif "📧 Email Intel" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📧 Email Intel: Auditoria & Resposta</h1></div>', unsafe_allow_html=True)
    col_u, col_r = st.columns([1, 2])
    with col_u:
        arquivos = st.file_uploader("Anexe e-mails (PDF):", type=["pdf"], accept_multiple_files=True)
        cargo = st.text_input("Seu Cargo para Resposta:", placeholder="Ex: Diretor de Operações")
        btn_audit = st.button("🔍 INICIAR AUDITORIA EM LOTE")
    with col_r:
        if arquivos and btn_audit:
            for i, pdf in enumerate(arquivos):
                with st.expander(f"Auditoria: {pdf.name}", expanded=True):
                    res_texto, mod_ativo = call_ai_with_failover(f"Resuma este e-mail e rascunhe resposta como {cargo}.", [{"mime_type": "application/pdf", "data": pdf.read()}])
                    st.markdown(res_texto)
                    st.download_button(f"📩 Baixar Resposta {i+1}", data=gerar_docx(f"Resposta: {pdf.name}", res_texto), file_name=f"Resposta_{pdf.name}.docx")

elif "📁 Analisador de Documentos" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📁 Analisador de Documentos</h1></div>', unsafe_allow_html=True)
    arquivo = st.file_uploader("Upload (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
    if arquivo and st.button("🔍 EXECUTAR ANÁLISE ESTRATÉGICA"):
        with st.spinner("IA processando dados..."):
            if arquivo.type == "application/pdf":
                dados = [{"mime_type": "application/pdf", "data": arquivo.read()}]
                prompt_doc = "Aja como Consultor McKinsey. Gere: Resumo Executivo, Impacto (Risco/Custo) e Plano de Ação."
            else:
                texto_raw = extrair_texto_docx(arquivo) if arquivo.name.endswith('docx') else arquivo.read().decode()
                dados = [texto_raw]
                prompt_doc = "Analise o texto a seguir sob a ótica de negócios:"
            res_doc, mod_doc = call_ai_with_failover(prompt_doc, dados)
            st.markdown(res_doc)
            st.download_button("📄 Baixar Relatório McKinsey", data=gerar_docx("Análise de Documento", res_doc), file_name="Analise_Estrategica.docx")

elif "🧠 Briefing Negocial" in menu_selecionado:
    st.markdown("### 🧠 Briefing Negocial Estratégico")
    emp_alvo = st.text_input("Empresa Alvo:")
    obj_an = st.text_area("Objetivo da Análise:")
    if st.button("⚡ ESCANEAR MERCADO"):
        res, mod = call_ai_with_failover(f"Gere um briefing 2026 para {emp_alvo}. Objetivo: {obj_an}")
        st.markdown(res)
        st.download_button("🧠 Baixar Briefing Nexus", data=gerar_docx(f"Briefing: {emp_alvo}", res), file_name=f"Briefing_{emp_alvo}.docx")

elif "📝 Analista de Atas" in menu_selecionado:
    st.markdown('<div class="product-header"><h1>📝 Analista de Atas</h1></div>', unsafe_allow_html=True)
    notas_r = st.text_area("Notas da reunião:", height=300)
    if st.button("📝 FORMALIZAR ATA"):
        res, mod = call_ai_with_failover(f"Transforme em ata formal de diretoria: {notas_r}")
        st.markdown(res)
        st.download_button("📝 Baixar Ata de Governança", data=gerar_docx("Ata de Reunião", res), file_name="Ata_Oficial.docx")

elif "📈 Inteligência Competitiva" in menu_selecionado:
    t1, t2 = st.tabs(["🔍 Radar Rival", "⚠️ Churn"])
    with t1:
        rival_n = st.text_input("Rival:")
        if st.button("📡 ANALISAR"):
            res, mod = call_ai_with_failover(f"Analise a estratégia da empresa {rival_n}.")
            st.markdown(res)
            st.download_button("📈 Baixar Radar", data=gerar_docx(f"Radar: {rival_n}", res), file_name=f"Radar_{rival_n}.docx")
    with t2:
        feed_c = st.text_area("Feedback do cliente:")
        if st.button("🧠 PREVER RISCO"):
            res, mod = call_ai_with_failover(f"Risco de churn para: {feed_c}")
            st.markdown(res)
            st.download_button("⚠️ Baixar Análise de Churn", data=gerar_docx("Previsão de Risco", res), file_name="Analise_Churn.docx")

# --- RODAPÉ ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption(f"TechnoBolt IA Hub © {time.strftime('%Y')} | Master Resilience Edition v11.1")