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

# --- 3. DESIGN SYSTEM (ELITE DARK V2) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* RESET GLOBAL E CORES DE FUNDO */
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
    
    /* FORÇAR TEXTO BRANCO EM TUDO */
    p, h1, h2, h3, h4, span, label, div, [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }

    /* ESTILIZAÇÃO DE FORMS E INPUTS (CINZA ESCURO) */
    [data-testid="stForm"], .main-card {
        background-color: #111111 !important;
        border: 1px solid #333 !important;
        border-radius: 15px !important;
        padding: 25px !important;
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
    }

    /* CARD DE RESULTADO DA IA (CINZA EXECUTIVO) */
    .result-card-elite {
        background-color: #1a1a1a;
        border-left: 5px solid #3b82f6;
        border-radius: 12px;
        padding: 30px;
        margin-top: 20px;
        border-top: 1px solid #333;
        border-right: 1px solid #333;
        border-bottom: 1px solid #333;
    }

    /* BOTÕES */
    .stButton > button {
        width: 100%; border-radius: 10px; height: 3.2em; font-weight: 700;
        background: #3b82f6 !important; color: white !important; border: none !important;
    }

    .status-badge {
        padding: 5px 15px; border-radius: 50px; background: #222;
        color: #3b82f6 !important; font-size: 11px; font-weight: 700; border: 1px solid #333;
    }

    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. UTILITÁRIOS (LIMPEZA DE SÍMBOLOS) ---
def limpar_formatacao(texto):
    """Remove marcações excessivas de IA para o cliente final."""
    texto = texto.replace('**', '').replace('###', '').replace('##', '').replace('#', '')
    texto = re.sub(r'\n{3,}', '\n\n', texto) # Remove quebras excessivas
    return texto.strip()

# --- 5. MOTOR DE IA (RODÍZIO E FAILOVER) ---
MODEL_FAILOVER_LIST = ["models/gemini-3-flash-preview", "models/gemini-2.5-flash", "models/gemini-2.0-flash", "models/gemini-flash-latest"]

def call_technobolt_ai(prompt, attachments=None, system_context="default"):
    chaves = [os.environ.get(f"GEMINI_CHAVE_{i}") for i in range(1, 8)]
    chaves = [k for k in chaves if k]
    if not chaves: chaves = [os.environ.get("GEMINI_API_KEY")]

    p = st.session_state.perfil_cliente
    dna_context = f"DNA: {p['nome_empresa']} | {p['setor']}. Tom: {p['tom_voz']}. FORMATAÇÃO: Limpa, sem símbolos Markdown desnecessários.\n"
    
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
    st.markdown("<div style='height: 20vh;'></div>", unsafe_allow_html=True)
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

# --- 7. NAVEGAÇÃO LATERAL (MENU COM SETA) ---
with st.sidebar:
    st.markdown(f"""
    <div style='text-align: center; padding: 20px;'>
        <h2 style='color: #3b82f6; margin: 0;'>TECHNOBOLT</h2>
        <p style='font-size: 10px; color: #555;'>GOVERNANÇA ELITE v2.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    escolha = st.radio(
        "MÓDULOS ESTRATÉGICOS ➔",
        ["🏠 Centro de Comando", "📁 Analisador de Documentos", "📧 Analisador de E-mails", 
         "✉️ Gerador de Emails", "🧠 Briefing Estratégico", "📝 Gerador de Atas", 
         "📈 Mercado & Churn", "📊 Relatório Semanal"],
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='height: 30vh;'></div>", unsafe_allow_html=True)
    st.markdown(f"**Operador:** <span class='status-badge'>{st.session_state.user_atual.upper()}</span>", unsafe_allow_html=True)
    if st.button("🚪 Encerrar Sessão"):
        st.session_state.logged_in = False
        st.rerun()

# --- 8. LÓGICA DE MÓDULOS ---

if "🏠 Centro" in escolha:
    st.markdown("<h1 class='hero-title'>Soberania Digital</h1>", unsafe_allow_html=True)
    st.markdown("""<div class='main-card' style='text-align:center;'>
        <img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXlsaTYwaDZkeGc2MjMxcXk4MWJjMGtwcHEwNTZ6dHFkaXV0NzNxbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eljCVpMrhepUSgZaVP/giphy.gif" width="300">
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Status IA", "Soberana")
    c2.metric("DNA Ativo", st.session_state.perfil_cliente["nome_empresa"])

elif "📁 Analisador" in escolha:
    st.markdown("<div class='main-card'><h2>📁 Analisador de Documentos</h2></div>", unsafe_allow_html=True)
    with st.form("form_docs"):
        up = st.file_uploader("Submeter PDF/DOCX", type=['pdf', 'docx'])
        if st.form_submit_button("EXECUTAR PROTOCOLO"):
            with st.spinner("Auditando..."):
                dados = [{"mime_type": "application/pdf", "data": up.read()}] if up.type == "application/pdf" else [up.read().decode(errors='ignore')]
                res, mot = call_technobolt_ai("Audite este documento.", dados, "mckinsey")
                st.session_state.resultado_ia = res
                st.session_state.titulo_resultado = f"Auditoria McKinsey ({mot})"
                st.session_state.mostrar_resultado = True
                st.rerun()

elif "📧 Analisador" in escolha:
    st.markdown("<div class='main-card'><h2>📧 Analisador de E-mails</h2></div>", unsafe_allow_html=True)
    with st.form("form_email"):
        txt = st.text_area("Lote de e-mails para triagem:", height=200)
        if st.form_submit_button("PROCESSAR"):
            res, mot = call_technobolt_ai(txt, None, "email_intel")
            st.session_state.resultado_ia = res
            st.session_state.titulo_resultado = f"Triagem CCO ({mot})"
            st.session_state.mostrar_resultado = True
            st.rerun()

elif "📝 Gerador de Atas" in escolha:
    st.markdown("<div class='main-card'><h2>📝 Gestor de Atas</h2></div>", unsafe_allow_html=True)
    with st.form("form_atas"):
        notas = st.text_area("Notas da Reunião:", height=200)
        if st.form_submit_button("FORMALIZAR"):
            res, mot = call_technobolt_ai(notas, None, "ata")
            st.session_state.resultado_ia = res
            st.session_state.titulo_resultado = f"Ata de Governança ({mot})"
            st.session_state.mostrar_resultado = True
            st.rerun()

# (Repetir lógica similar para os demais módulos seguindo o padrão de st.form cinza)

# --- 9. EXIBIÇÃO DE RESULTADO (CARD CINZA LIMPO) ---
if st.session_state.mostrar_resultado:
    st.markdown("---")
    _, mid, _ = st.columns([1, 8, 1])
    with mid:
        # Sanitização do texto para exibição
        texto_limpo = limpar_formatacao(st.session_state.resultado_ia)
        
        st.markdown(f"""
        <div class='result-card-elite'>
            <h2 style='color:#3b82f6 !important;'>{st.session_state.titulo_resultado}</h2>
            <div style='color:#ccc !important; white-space: pre-wrap; font-size: 15px;'>
{texto_limpo}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Ações de Exportação
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
st.caption(f"TechnoBolt Solutions © 2026 | Operador: {st.session_state.user_atual.upper()} | Hub Elite v2.0")
