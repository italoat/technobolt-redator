import streamlit as st
import google.generativeai as genai
import json
import os

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="TechnoBolt - AI Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS: APENAS REMOVE BARRA SUPERIOR (MANTÉM TEMA CLARO PADRÃO) ---
hide_header_style = """
<style>
    /* Remove o cabeçalho (menu hambúrguer e barra colorida) */
    header {visibility: hidden;}
    
    /* Remove o rodapé padrão */
    footer {visibility: hidden;}
    
    /* Ajusta o padding para o conteúdo subir */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* (Opcional) Força fundo branco caso o navegador force escuro */
    .stApp {
        background-color: #ffffff;
        color: #262730;
    }
</style>
"""
st.markdown(hide_header_style, unsafe_allow_html=True)

# --- 3. LÓGICA DE DADOS E API ---

# Busca a chave nas variáveis de ambiente
api_key = os.environ.get("GEMINI_API_KEY")

CONFIG_FILE = "perfil_empresa.json"

def carregar_perfil():
    """Carrega o perfil do arquivo JSON ou retorna valores padrão."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "nome_empresa": "",
        "setor": "",
        "publico_alvo": "",
        "tom_voz": "",
        "proibicoes": "",
        "exemplo_estilo": ""
    }

def salvar_perfil(dados):
    """Salva o perfil no arquivo JSON."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# Inicialização da Sessão
if "perfil" not in st.session_state:
    st.session_state.perfil = carregar_perfil()

# --- 4. BARRA LATERAL ---
with st.sidebar:
    st.title("⚡ TechnoBolt")
    st.caption("Intelligence System v1.2")
    st.markdown("---")
    
    # Status da Conexão
    if api_key:
        st.success("✅ Servidor Conectado")
    else:
        st.error("❌ API Key Ausente")
        st.info("Configure a variável GEMINI_API_KEY no seu ambiente (ou no Render).")

# --- 5. TÍTULO PRINCIPAL ---
st.title("🚀 Suite de Comunicação Corporativa")
st.markdown("---")

# --- 6. ABAS ---
tab1, tab2 = st.tabs(["🏭 DNA da Empresa", "✍️ Gerador de Conteúdo"])

# --- ABA 1: PERFIL ---
with tab1:
    st.header("Configuração Estratégica")
    st.info("Preencha os dados abaixo para treinar a IA com a identidade da sua empresa.")
    
    col1, col2 = st.columns(2)
    with col1:
        nome_empresa = st.text_input("Nome da Empresa", value=st.session_state.perfil["nome_empresa"])
        setor = st.text_input("Setor de Atuação", value=st.session_state.perfil["setor"])
        publico_alvo = st.text_area("Público-Alvo", value=st.session_state.perfil["publico_alvo"], height=100)
    
    with col2:
        tom_voz = st.text_area("Tom de Voz", value=st.session_state.perfil["tom_voz"], height=100, placeholder="Ex: Profissional, direto, acolhedor...")
        proibicoes = st.text_input("Termos Proibidos", value=st.session_state.perfil["proibicoes"])
        exemplo_estilo = st.text_area("Exemplo de Email (Opcional):", value=st.session_state.perfil["exemplo_estilo"], height=100)

    if st.button("💾 Salvar DNA da Marca", type="primary"):
        novos_dados = {
            "nome_empresa": nome_empresa,
            "setor": setor,
            "publico_alvo": publico_alvo,
            "tom_voz": tom_voz,
            "proibicoes": proibicoes,
            "exemplo_estilo": exemplo_estilo
        }
        salvar_perfil(novos_dados)
        st.session_state.perfil = novos_dados
        st.toast("Perfil atualizado com sucesso!", icon="⚡")

# --- ABA 2: GERADOR ---
with tab2:
    st.header("Gerador de Conteúdo AI")
    
    # Verifica se o perfil está preenchido
    if not st.session_state.perfil["nome_empresa"]:
        st.warning("⚠️ Configure o perfil na aba anterior antes de começar.")
    else:
        st.markdown(f"Cliente Ativo: **{st.session_state.perfil['nome_empresa']}**")
        
        col_input, col_output = st.columns([1, 1])

        with col_input:
            tipo_conteudo = st.selectbox("Tipo de Documento", 
                ["E-mail Profissional", "Post para Redes Sociais", "Comunicado Interno", "Resposta a Cliente", "Artigo para Blog", "Roteiro de Vendas"])
            
            topico = st.text_area("Instruções / Tópicos", height=250, placeholder="Descreva sobre o que a IA deve escrever...")
            
            gerar_btn = st.button("⚡ PROCESSAR TEXTO", type="primary")

        with col_output:
            if gerar_btn:
                if not api_key:
                    st.error("⛔ ERRO CRÍTICO: Chave de API não encontrada.")
                    st.markdown("Verifique se a variável `GEMINI_API_KEY` está configurada.")
                elif not topico:
                    st.warning("⚠️ Digite um tópico para processar.")
                else:
                    with st.spinner("A IA está escrevendo..."):
                        try:
                            # Configuração da IA
                            genai.configure(api_key=api_key)
                            
                            # Modelo atualizado para versão estável (Flash 1.5)
                            model = genai.GenerativeModel('gemini-2.5-flash')

                            # Prompt Engenharia
                            p = st.session_state.perfil
                            prompt_sistema = f"""
                            Atue como o Redator Sênior da empresa {p['nome_empresa']} ({p['setor']}).
                            Seu público é: {p['publico_alvo']}.

                            DIRETRIZES DE TOM DE VOZ:
                            {p['tom_voz']}
                            
                            RESTRIÇÕES (O QUE NÃO DIZER):
                            {p['proibicoes']}
                            
                            EXEMPLO DE REFERÊNCIA:
                            {p['exemplo_estilo']}

                            TAREFA ATUAL:
                            Escreva um(a) {tipo_conteudo}.
                            TEMA/INSTRUÇÕES: {topico}

                            Gere apenas o texto final. Formate com Markdown profissional.
                            """

                            response = model.generate_content(prompt_sistema)
                            
                            st.success("Processamento Concluído!")
                            st.markdown("### Resultado:")
                            st.markdown(response.text) # Renderiza o Markdown direto
                            
                        except Exception as e:
                            st.error(f"Erro na geração: {e}")

if __name__ == "__main__":
    pass