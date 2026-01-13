import streamlit as st
import google.generativeai as genai
import os
import time
import docx  # Requer: pip install python-docx
from io import BytesIO
import re

# --- 1. CONFIGURAÇÃO DE SEGURANÇA E PROTOCOLO ---
st.set_page_config(
    page_title="TechnoBolt IA - Elite Hub de Governança",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GESTÃO DE ESTADO (DNA CORPORATIVO) ---
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
    'mostrar_resultado': False,
    'resultado_ia': "",
    'titulo_resultado': ""
}

for chave, valor in chaves_sessao.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor

# --- 3. DESIGN SYSTEM (ELITE CORPORATE UI - DEEP DARK) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* RESET GLOBAL E FUNDO */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* BARRA LATERAL (SIDEBAR) */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a !important;
        border-right: 1px solid #222;
    }

    /* FORÇAR SETA DO MENU BRANCA */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        color: white !important;
    }
    button[data-testid="stSidebarCollapseButton"] svg {
        fill: white !important;
    }

    /* MENU LATERAL PROFISSIONAL (SEM CÍRCULOS E PADRONIZADO) */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        gap: 2px;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] input {
        display: none !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background-color: #111;
        border: 1px solid #222;
        padding: 0px 20px !important;
        border-radius: 6px;
        margin-bottom: 4px;
        color: #ffffff !important;
        height: 48px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        transition: 0.3s;
        cursor: pointer;
        width: 100% !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        border-color: #444;
        background-color: #1a1a1a;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] div[data-testid="stMarkdownContainer"] p {
        font-size: 13px !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #ffffff !important;
    }

    /* FORÇAR TEXTO BRANCO EM TUDO */
    p, h1, h2, h3, h4, span, label, div, [data-testid="stMarkdownContainer"] p, input, textarea {
        color: #ffffff !important;
    }

    /* FORMULÁRIOS E INPUTS CINZA CARVÃO (ELIMINANDO BRANCOS) */
    [data-testid="stForm"], .main-card {
        background-color: #111111 !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        padding: 25px !important;
    }

    /* COMPONENTES DE SELEÇÃO E TEXTO */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        color: white !important;
    }

    /* CORREÇÃO DO ÁREA DE UPLOAD (DRAG AND DROP) */
    [data-testid="stFileUploader"] section {
        background-color: #111111 !important;
        border: 1px dashed #444 !important;
        border-radius: 10px;
    }
    [data-testid="stFileUploader"] section div {
        color: #ffffff !important;
    }

    /* REFORÇO DOS BOTÕES (DARK GREY - CINZA ESCURO) */
    .stButton > button, [data-testid="stDownloadButton"] button {
        width: 100% !important;
        border-radius: 8px !important;
        height: 3.2em !important;
        font-weight: 700 !important;
        background-color: #262626 !important; 
        color: white !important; 
        border: 1px solid #444 !important;
        transition: 0.4s !important;
    }
    
    .stButton > button:hover, [data-testid="stDownloadButton"] button:hover {
        background-color: #333333 !important;
        border-color: #555 !important;
        transform: translateY(-1px);
        color: white !important;
    }

    /* RESULTADO IA */
    .result-card-elite {
        background-color: #111111;
        border-left: 5px solid #444;
        border-radius: 10px;
        padding: 30px;
        margin-top: 20px;
        border: 1px solid #333;
    }

    .hero-title { 
        font-size: 32px; font-weight: 800; text-align: center;
        background: linear-gradient(135deg, #ffffff 0%, #444444 100%); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        margin-bottom: 25px;
    }

    footer { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. UTILITÁRIOS ---
def limpar_formatacao(texto):
    texto = texto.replace('**', '').replace('###', '').replace('##', '').replace('#', '')
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    return texto.strip()

# --- 5. MOTOR DE IA (ÍNTEGRO) ---
MODEL_FAILOVER_LIST = ["models/gemini-3-flash-preview", "models/gemini-2.5-flash", "models/gemini-2.0-flash", "models/gemini-flash-latest"]

def call_technobolt_ai(prompt, attachments=None, system_context="default"):
    chaves = [os.environ.get(f"GEMINI_CHAVE_{i}") for i in range(1, 8)]
    chaves = [k for k in chaves if k]
    if not chaves: chaves = [os.environ.get("GEMINI_API_KEY")]

    p = st.session_state.perfil_cliente
    dna_context = f"DNA: {p['nome_empresa']} | {p['setor']}. Tom: {p['tom_voz']}. FORMATAÇÃO: Limpa, sem símbolos.\n"
    
    contexts = {
        "mckinsey": "Persona: Sócio McKinsey. Framework: 7S e MECE. Resumo Executivo, Diagnóstico e Plano de Ação.",
        "email_intel": "Persona: CCO. Triagem diplomática de e-mails e rascunhos de alta gestão.",
        "briefing": "Persona: Diretor de Inteligência. Análise PESTEL e Forças de Porter.",
        "ata": "Persona: Secretário de Governança B3. Ata formal com Matriz RACI.",
        "churn": "Persona: Especialista em Retenção. Diagnóstico de risco e plano de contenção.",
        "master": "Persona: COO. Consolidação semanal de KPIs e marcos operacionais.",
        "default": "Consultoria Sênior TechnoBolt. Direto e Analítico."
    }
    
    sys_instr = dna_context + contexts.get(system_context, contexts["default"])
    
    for idx, key in enumerate(chaves):
        try:
            genai.configure(api_key=key)
            for model_name in MODEL_FAILOVER_LIST:
                try:
                    model = genai.GenerativeModel(model_name, system_instruction=sys_instr)
                    payload = [prompt] + attachments if attachments else prompt
                    response = model.generate_content(payload)
                    return response.text, f"Eixo {idx+1}-{model_name.split('/')[-1]}"
                except: continue
        except: continue
    return "⚠️ Motores em manutenção.", "OFFLINE"

# --- 6. AUTENTICAÇÃO ---
if not st.session_state.logged_in:
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1.2, 1])
    with col_login:
        with st.form("auth_hub"):
            st.markdown("<h1 class='hero-title'>TECHNOBOLT HUB</h1>", unsafe_allow_html=True)
            u = st.text_input("Operador", placeholder="ID")
            k = st.text_input("Chave", type="password", placeholder="PIN")
            if st.form_submit_button("CONECTAR"):
                users = {"admin": "admin", "luiza.trovao": "teste@2025", "anderson.bezerra": "teste@2025"}
                if u in users and users[u] == k:
                    st.session_state.logged_in = True
                    st.session_state.user_atual = u
                    st.rerun()
    st.stop()

# --- 7. NAVEGAÇÃO LATERAL (LIMPA E PROFISSIONAL) ---
with st.sidebar:
    st.markdown(f"""
    <div style='text-align: center; padding: 15px 0;'>
        <h2 style='color: #ffffff; margin: 0; font-size: 20px; font-weight: 700;'>TECHNOBOLT</h2>
        <p style='font-size: 9px; color: #555; text-transform: uppercase;'>Governança Elite v2.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu_opcoes = [
        "Centro de Comando", 
        "Analisador de Documentos", 
        "Analisador de E-mails", 
        "Gerador de Emails", 
        "Briefing Estratégico", 
        "Gerador de Atas", 
        "Mercado & Churn", 
        "Relatório Semanal"
    ]
    
    escolha = st.radio("NAV_ROOT", menu_opcoes, label_visibility="collapsed")
    
    st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background:#111; padding:15px; border-radius:10px; border:1px solid #222;'><b>Operador:</b><br><span style='color:#ffffff;'>{st.session_state.user_atual.upper()}</span></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Encerrar Sessão"):
        st.session_state.logged_in = False
        st.rerun()

# --- 8. LÓGICA DE MÓDULOS ---

if escolha == "Centro de Comando":
    st.markdown("<h1 class='hero-title'>Painel de Governança</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class='main-card'>
        <h3 style='color:#ffffff;'>Guia de Operação Estratégica</h3>
        <p style='color:#888; margin-bottom:20px;'>Selecione um módulo no menu lateral para iniciar.</p>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px;'>
            <div style='background:#161616; padding:15px; border-radius:10px;'><b>ANÁLISE DE DOCUMENTOS</b><br>Retorna avaliação gerencial técnica.</div>
            <div style='background:#161616; padding:15px; border-radius:10px;'><b>ANÁLISE DE E-MAILS</b><br>Triagem cognitiva de massa.</div>
            <div style='background:#161616; padding:15px; border-radius:10px;'><b>GERADOR DE ATAS</b><br>Formalização B3 com RACI.</div>
            <div style='background:#161616; padding:15px; border-radius:10px;'><b>BRIEFING NEGOCIAL</b><br>Scan competitivo PESTEL/Porter.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif escolha == "Analisador de Documentos":
    st.markdown("<div class='main-card'><h2>Analisador de Documentos</h2></div>", unsafe_allow_html=True)
    with st.form("form_docs"):
        up = st.file_uploader("Submeter PDF/DOCX", type=['pdf', 'docx'])
        if st.form_submit_button("EXECUTAR PROTOCOLO"):
            if up:
                with st.spinner("Auditando..."):
                    dados = [{"mime_type": "application/pdf", "data": up.read()}] if up.type == "application/pdf" else [up.read().decode(errors='ignore')]
                    res, mot = call_technobolt_ai("Audite este documento.", dados, "mckinsey")
                    st.session_state.resultado_ia = res
                    st.session_state.titulo_resultado = f"Documento Revisado"
                    st.session_state.mostrar_resultado = True
                    st.rerun()

elif escolha == "Analisador de E-mails":
    st.markdown("<div class='main-card'><h2>Analisador de E-mails</h2></div>", unsafe_allow_html=True)
    with st.form("form_emails"):
        lote = st.text_area("Cole aqui os blocos de e-mail para triagem:", height=250)
        if st.form_submit_button("EXECUTAR TRIAGEM"):
            with st.spinner("CCO analisando comunicações..."):
                res, mot = call_technobolt_ai(lote, None, "email_intel")
                st.session_state.resultado_ia = res
                st.session_state.titulo_resultado = f"Triagem Executiva"
                st.session_state.mostrar_resultado = True
                st.rerun()

elif escolha == "Gerador de Emails":
    st.markdown("<div class='main-card'><h2>Gerador de Emails de Elite</h2></div>", unsafe_allow_html=True)
    with st.form("form_gen_mail"):
        pauta = st.text_area("Descreva o assunto ou pauta do e-mail:")
        if st.form_submit_button("GERAR REDAÇÃO"):
            with st.spinner("Redigindo e-mail diplomático..."):
                res, mot = call_technobolt_ai(f"Gere um email profissional sobre: {pauta}", None, "default")
                st.session_state.resultado_ia = res
                st.session_state.titulo_resultado = f"Email Redigido"
                st.session_state.mostrar_resultado = True
                st.rerun()

elif escolha == "Briefing Estratégico":
    st.markdown("<div class='main-card'><h2>Briefing Estratégico</h2></div>", unsafe_allow_html=True)
    with st.form("form_briefing"):
        alvo = st.text_input("Empresa ou Setor para Análise:")
        if st.form_submit_button("GERAR SCAN"):
            with st.spinner("Coletando inteligência..."):
                res, mot = call_technobolt_ai(f"Gere um briefing estratégico sobre: {alvo}", None, "briefing")
                st.session_state.resultado_ia = res
                st.session_state.titulo_resultado = f"Scan de Mercado: {alvo}"
                st.session_state.mostrar_resultado = True
                st.rerun()

elif escolha == "Gerador de Atas":
    st.markdown("<div class='main-card'><h2>Gerador de Atas</h2></div>", unsafe_allow_html=True)
    with st.form("form_atas"):
        notas = st.text_area("Notas ou Transcrições da Reunião:", height=250)
        if st.form_submit_button("FORMALIZAR ATA"):
            with st.spinner("Estruturando Governança..."):
                res, mot = call_technobolt_ai(notas, None, "ata")
                st.session_state.resultado_ia = res
                st.session_state.titulo_resultado = f"Ata Formalizada"
                st.session_state.mostrar_resultado = True
                st.rerun()

elif escolha == "Mercado & Churn":
    st.markdown("<div class='main-card'><h2>Inteligência de Mercado & Churn</h2></div>", unsafe_allow_html=True)
    with st.form("form_churn"):
        dados_cli = st.text_area("Feedbacks ou métricas de comportamento do cliente:")
        if st.form_submit_button("CALCULAR RISCO"):
            with st.spinner("Avaliando retenção..."):
                res, mot = call_technobolt_ai(dados_cli, None, "churn")
                st.session_state.resultado_ia = res
                st.session_state.titulo_resultado = f"Análise de Retenção"
                st.session_state.mostrar_resultado = True
                st.rerun()

elif escolha == "Relatório Semanal":
    st.markdown("<div class='main-card'><h2>Relatório Semanal de KPIs</h2></div>", unsafe_allow_html=True)
    with st.form("form_semanal"):
        kpis = st.text_area("Fatos, métricas e marcos da semana:")
        if st.form_submit_button("CONSOLIDAR RELATÓRIO"):
            with st.spinner("COO consolidando dados..."):
                res, mot = call_technobolt_ai(kpis, None, "master")
                st.session_state.resultado_ia = res
                st.session_state.titulo_resultado = f"Relatório Semanal"
                st.session_state.mostrar_resultado = True
                st.rerun()

# --- 9. EXIBIÇÃO DE RESULTADO ---
if st.session_state.mostrar_resultado:
    st.markdown("---")
    _, mid, _ = st.columns([1, 8, 1])
    with mid:
        texto_limpo = limpar_formatacao(st.session_state.resultado_ia)
        st.markdown(f"""
        <div class='result-card-elite'>
            <h2 style='color:#ffffff !important;'>{st.session_state.titulo_resultado}</h2>
            <div style='color:#eee !important; white-space: pre-wrap; font-size: 15px;'>
{texto_limpo}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if c1.button("📥 BAIXAR DOCX"):
            doc = docx.Document()
            doc.add_heading(st.session_state.titulo_resultado, 0)
            doc.add_paragraph(texto_limpo)
            buf = BytesIO(); doc.save(buf); buf.seek(0)
            st.download_button("Download Confirmado", buf, "relatorio_technobolt.docx")
        if c2.button("✖️ FECHAR"):
            st.session_state.mostrar_resultado = False
            st.rerun()

# --- 10. RODAPÉ ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption(f"TechnoBolt Solutions © 2026 | Hub Elite v2.0")
