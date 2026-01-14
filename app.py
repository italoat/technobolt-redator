import streamlit as st
import google.generativeai as genai
import os
import time
import docx  # Requer: pip install python-docx
from io import BytesIO
import re
import json
from datetime import datetime
from pymongo import MongoClient
import pandas as pd

# --- 1. CONFIGURAÇÃO DE SEGURANÇA E PROTOCOLO ---
st.set_page_config(
    page_title="TechnoBolt IA - Elite Hub de Governança",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CONEXÃO MONGODB (RENDER CONFIG) ---
@st.cache_resource
def iniciar_conexao():
    uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(uri)
    return client["technobolthub"]

db = iniciar_conexao()

# --- 3. GESTÃO DE ESTADO (DNA CORPORATIVO) ---
chaves_sessao = {
    'logged_in': False,
    'user_atual': None,
    'user_plan': 'Standard',
    'is_admin': False,
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

# --- 4. DESIGN SYSTEM (ELITE CORPORATE UI) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stSidebar"] { background-color: #0a0a0a !important; border-right: 1px solid #222; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; color: white !important; }
    button[data-testid="stSidebarCollapseButton"] svg { fill: white !important; }
    [data-testid="stSidebar"] div[role="radiogroup"] input { display: none !important; }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background-color: #111; border: 1px solid #222; padding: 0px 20px !important;
        border-radius: 6px; margin-bottom: 4px; color: #ffffff !important;
        height: 48px !important; display: flex !important; align-items: center !important;
        justify-content: flex-start !important; transition: 0.3s; cursor: pointer; width: 100% !important;
    }
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover { border-color: #444; background-color: #1a1a1a; }
    p, h1, h2, h3, h4, span, label, div, [data-testid="stMarkdownContainer"] p, input, textarea { color: #ffffff !important; }
    [data-testid="stForm"], .main-card {
        background-color: #111111 !important; border: 1px solid #333 !important;
        border-radius: 12px !important; padding: 25px !important;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #1a1a1a !important; border: 1px solid #333 !important;
        border-radius: 8px !important; color: white !important;
    }
    .stButton > button {
        width: 100% !important; border-radius: 8px !important; height: 3.2em !important;
        font-weight: 700 !important; background: #262626 !important; color: #ffffff !important; 
        border: 1px solid #444 !important; transition: 0.4s !important;
    }
    .stButton > button:hover { background: #333333 !important; border-color: #555 !important; }
    .hero-title { 
        font-size: 32px; font-weight: 800; text-align: center;
        background: linear-gradient(135deg, #ffffff 0%, #444444 100%); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 25px;
    }
    footer { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# --- 5. UTILITÁRIOS E PERSISTÊNCIA ---
def limpar_formatacao(texto):
    texto = texto.replace('**', '').replace('###', '').replace('##', '').replace('#', '')
    texto = re.sub(r'```json.*?```', '', texto, flags=re.DOTALL)
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    return texto.strip()

def persistir_interacao(modulo, input_data, output_text, kpis_json):
    log = {
        "usuario": st.session_state.user_atual,
        "timestamp": datetime.now(),
        "modulo": modulo,
        "input": str(input_data)[:500],
        "output": output_text[:1000],
        "kpis": kpis_json
    }
    db["governanca_logs"].insert_one(log)

def validar_usuario(username):
    if not username: return False
    return not bool(re.search(r'[\s@]', username))

# --- 6. MOTOR DE IA ---
MODEL_FAILOVER_LIST = ["models/gemini-3-flash-preview", "models/gemini-2.5-flash", "models/gemini-2.0-flash", "models/gemini-flash-latest"]

def call_technobolt_ai(prompt, attachments=None, system_context="default"):
    chaves = [os.environ.get(f"GEMINI_CHAVE_{i}") for i in range(1, 8)]
    chaves = [k for k in chaves if k] or [os.environ.get("GEMINI_API_KEY")]

    p = st.session_state.perfil_cliente
    dna_context = f"DNA: {p['nome_empresa']}. Tom: {p['tom_voz']}.\n"
    
    kpi_instruction = (
        "\nOBRIGATÓRIO: No final da resposta, adicione EXATAMENTE um bloco JSON estruturado entre ```json e ``` "
        "com as chaves: 'faturamento', 'margem', 'riscos_count', 'prazos_alerta'."
    )

    contexts = {
        "mckinsey": "Persona: Sócio McKinsey. Framework: 7S e MECE.",
        "email_intel": "Persona: CCO. Triagem diplomática.",
        "briefing": "Persona: Diretor de Inteligência.",
        "ata": "Persona: Secretário de Governança B3.",
        "churn": "Persona: Especialista em Retenção.",
        "master": "Persona: COO. Consolidação semanal.",
        "default": "Consultoria Sênior TechnoBolt."
    }
    
    sys_instr = dna_context + contexts.get(system_context, contexts["default"]) + kpi_instruction
    
    for key in chaves:
        try:
            genai.configure(api_key=key)
            for model_name in MODEL_FAILOVER_LIST:
                try:
                    model = genai.GenerativeModel(model_name, system_instruction=sys_instr)
                    payload = [prompt] + attachments if attachments else prompt
                    response = model.generate_content(payload)
                    full_text = response.text
                    kpis = {"faturamento": 0, "margem": 0, "riscos_count": 0, "prazos_alerta": 0}
                    json_match = re.search(r'```json\n(.*?)\n```', full_text, re.DOTALL)
                    if json_match:
                        try: kpis = json.loads(json_match.group(1))
                        except: pass
                    clean_res = limpar_formatacao(full_text)
                    persistir_interacao(system_context, prompt, clean_res, kpis)
                    return clean_res, f"{model_name.split('/')[-1]}"
                except: continue
        except: continue
    return "⚠️ Motores em manutenção.", "OFFLINE"

# --- 7. AUTENTICAÇÃO ---
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Hub Acesso", "Solicitar Acesso"])
    with tab1:
        with st.form("auth_hub"):
            st.markdown("<h1 class='hero-title'>TECHNOBOLT HUB</h1>", unsafe_allow_html=True)
            u = st.text_input("Operador ID", placeholder="ID")
            k = st.text_input("Chave PIN", type="password")
            if st.form_submit_button("CONECTAR"):
                user_db = db["usuarios"].find_one({"usuario": u, "senha": k})
                if user_db:
                    if user_db.get("status") == "ativo":
                        st.session_state.logged_in = True
                        st.session_state.user_atual = u
                        st.session_state.user_plan = user_db.get("plano", "Standard")
                        st.session_state.is_admin = user_db.get("is_admin", False)
                        st.rerun()
                    else: st.warning("Conta aguardando ativação administrativa.")
                else: st.error("ID ou PIN incorretos.")
    with tab2:
        with st.form("request_access"):
            new_u = st.text_input("ID Desejado (Sem espaços ou @)")
            new_k = st.text_input("PIN de Segurança", type="password")
            plan_req = st.selectbox("Plano Desejado", ["Standard", "Advanced", "Executive"])
            if st.form_submit_button("SOLICITAR"):
                if validar_usuario(new_u):
                    if not db["usuarios"].find_one({"usuario": new_u}):
                        db["usuarios"].insert_one({
                            "usuario": new_u, "senha": new_k, 
                            "plano": plan_req, "status": "inativo",
                            "is_admin": False,
                            "criado_em": datetime.now()
                        })
                        st.success("Solicitação em processamento.")
                    else: st.error("Este ID já está registrado.")
                else: st.error("O ID não pode conter espaços ou o caractere '@'.")
    st.stop()

# --- 8. NAVEGAÇÃO E PAYWALL ---
with st.sidebar:
    st.markdown(f"<h2 style='color:#ffffff; text-align:center;'>TECHNOBOLT</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:10px;'>MODO: {st.session_state.user_plan.upper()}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    opcoes = ["Centro de Comando", "Analisador de Documentos", "Analisador de E-mails", "Gerador de Emails", "Briefing Estratégico", "Gerador de Atas", "Mercado & Churn", "Relatório Semanal"]
    
    # AJUSTE: Permite acesso à gestão para ID "admin" ou qualquer um com flag is_admin
    if st.session_state.user_atual == "admin" or st.session_state.is_admin:
        opcoes.append("Gestão de Acesso")
        
    escolha = st.radio("NAV", opcoes, label_visibility="collapsed")
    st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
    if st.button("🚪 Sair"):
        st.session_state.logged_in = False
        st.rerun()

restritos_standard = ["Analisador de Documentos", "Analisador de E-mails", "Mercado & Churn"]
if st.session_state.user_plan == "Standard" and escolha in restritos_standard:
    st.markdown(f"<div class='main-card'><h2>🚀 Upgrade Necessário</h2><p>O módulo <b>{escolha}</b> está disponível apenas para parceiros Advanced e Executive.</p></div>", unsafe_allow_html=True)
    st.stop()

# --- 9. MÓDULOS ---

if escolha == "Centro de Comando":
    st.markdown("<h1 class='hero-title'>Dashboard Cognitivo</h1>", unsafe_allow_html=True)
    logs = list(db["governanca_logs"].find({"usuario": st.session_state.user_atual}).sort("timestamp", -1).limit(10))
    if logs:
        c1, c2, c3 = st.columns(3)
        riscos = sum([l.get("kpis", {}).get("riscos_count", 0) for l in logs])
        alertas = sum([l.get("kpis", {}).get("prazos_alerta", 0) for l in logs])
        c1.metric("Riscos Identificados", riscos)
        c2.metric("Prazos Críticos", alertas)
        c3.metric("Ações Recentes", len(logs))
        df = pd.DataFrame([{"Data": l["timestamp"], "Riscos": l.get("kpis", {}).get("riscos_count", 0)} for l in logs])
        st.line_chart(df.set_index("Data"))
    else:
        st.info("Execute análises para popular o dashboard estratégico.")

elif escolha == "Analisador de Documentos":
    st.markdown("<div class='main-card'><h2>Analisador de Documentos</h2></div>", unsafe_allow_html=True)
    with st.form("form_docs"):
        up = st.file_uploader("Submeter PDF/DOCX", type=['pdf', 'docx'])
        if st.form_submit_button("EXECUTAR PROTOCOLO"):
            if up:
                with st.spinner("Auditando..."):
                    content = up.read()
                    res, mot = call_technobolt_ai("Audite este documento e gere KPIs.", [content], "mckinsey")
                    st.session_state.resultado_ia = res
                    st.session_state.titulo_resultado = f"Auditoria McKinsey ({mot})"
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
                st.session_state.titulo_resultado = f"Triagem Executiva ({mot})"
                st.session_state.mostrar_resultado = True
                st.rerun()

elif escolha == "Gerador de Emails":
    st.markdown("<div class='main-card'><h2>Gerador de Emails</h2></div>", unsafe_allow_html=True)
    with st.form("form_gen_mail"):
        pauta = st.text_area("Descreva o assunto ou pauta do e-mail:")
        if st.form_submit_button("GERAR EMAIL"):
            with st.spinner("Redigindo e-mail diplomático..."):
                res, mot = call_technobolt_ai(f"Gere um email profissional sobre: {pauta}", None, "default")
                st.session_state.resultado_ia = res
                st.session_state.titulo_resultado = f"Email Redigido ({mot})"
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
                st.session_state.titulo_resultado = f"Scan de Mercado: {alvo} ({mot})"
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
                st.session_state.titulo_resultado = f"Ata Formalizada ({mot})"
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
                st.session_state.titulo_resultado = f"Análise de Retenção ({mot})"
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
                st.session_state.titulo_resultado = f"Relatório Semanal ({mot})"
                st.session_state.mostrar_resultado = True
                st.rerun()

elif escolha == "Gestão de Acesso" and (st.session_state.user_atual == "admin" or st.session_state.is_admin):
    st.markdown("## 🔐 Governança de Acessos")
    usuarios_lista = list(db["usuarios"].find())
    for u_data in usuarios_lista:
        is_user_admin = u_data.get('is_admin', False)
        perfil_md = f"""
        ### Operador: `{u_data['usuario']}` {' [ADMIN]' if is_user_admin else ''}
        ---
        - **Plano Atual:** {u_data['plano']}
        - **Status:** {u_data['status']}
        """
        st.markdown(perfil_md)
        col_p, col_s, col_adm = st.columns([1, 1, 1])
        with col_p:
            new_p = st.selectbox("Mudar Plano", ["Standard", "Advanced", "Executive"], index=["Standard", "Advanced", "Executive"].index(u_data['plano']), key=f"plan_{u_data['usuario']}")
        with col_s:
            new_s = st.selectbox("Mudar Status", ["ativo", "inativo"], index=["ativo", "inativo"].index(u_data['status']), key=f"stat_{u_data['usuario']}")
        with col_adm:
            st.markdown("<br>", unsafe_allow_html=True)
            # AJUSTE: Botão para tornar administrador
            if not is_user_admin:
                if st.button("Promover a Administrador", key=f"make_adm_{u_data['usuario']}"):
                    db["usuarios"].update_one({"usuario": u_data["usuario"]}, {"$set": {"is_admin": True}})
                    st.success(f"{u_data['usuario']} agora possui privilégios de Admin.")
                    st.rerun()
            else:
                st.info("Já possui acesso Admin.")

        if st.button("Aplicar Alterações de Plano/Status", key=f"save_{u_data['usuario']}"):
            db["usuarios"].update_one({"usuario": u_data["usuario"]}, {"$set": {"plano": new_p, "status": new_s}})
            st.success(f"Dossiê de {u_data['usuario']} atualizado.")
            st.rerun()
        st.markdown("---")

# --- 10. EXIBIÇÃO DE RESULTADOS ---
if st.session_state.mostrar_resultado:
    st.markdown("---")
    _, mid, _ = st.columns([1, 8, 1])
    with mid:
        texto_limpo = st.session_state.resultado_ia
        st.markdown(f"<div class='result-card-elite'><h2 style='color:#ffffff !important;'>{st.session_state.titulo_resultado}</h2><div style='color:#eee !important; white-space: pre-wrap; font-size: 15px;'>{texto_limpo}</div></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("📥 BAIXAR DOCX"):
            doc = docx.Document()
            doc.add_heading(st.session_state.titulo_resultado, 0)
            doc.add_paragraph(texto_limpo)
            buf = BytesIO(); doc.save(buf); buf.seek(0)
            st.download_button("Confirmação de Download", buf, "relatorio_technobolt.docx")
        if c2.button("✖️ FECHAR"):
            st.session_state.mostrar_resultado = False
            st.rerun()

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption(f"TechnoBolt Solutions © 2026 | Hub Elite v2.0")
