import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components

# Importar as funções de processamento
from answer_assistant import answer_assistant
from make_audio_assistant import make_audio_assistant
from transcribe_audio import transcribe_audio


# --- Callback Function ---
def process_audio_callback():
    """
    Callback para processar o áudio.
    Esta função é executada ANTES da re-execução do script quando um novo áudio é enviado.
    """
    # Se não houver áudio no estado do widget, não faz nada.
    if (
        "audio_input_user" not in st.session_state
        or not st.session_state.audio_input_user
    ):
        return

    # Armazena os bytes do áudio para serem processados no corpo principal do script
    audio_file = st.session_state.audio_input_user
    st.session_state.audio_bytes_to_process = audio_file.read()


# --- Configuração da Página ---
st.set_page_config(page_title="English Conversation Practice", layout="wide")
st.title("Pratique a sua conversação em inglês")
st.markdown(
    "Bem vindo! para praticar a sua conversação em inglês, basta clicar no botão Microfone, falar e depois clicar no botão Stop."
)

# --- Gerenciamento de Estado da Sessão ---
# Usamos st.session_state para manter os dados entre as re-execuções do script.
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {
            "role": "system",
            "content": "You are an English instructor leading a conversation practice session. \
            Your student is learning English, so their pronunciation and grammar might not be perfect. \
            Your role is to maintain a natural and friendly conversation. \
            If you notice significant errors in grammar or word choice that hinder understanding, \
            gently correct them and provide a brief, helpful explanation. For example: 'That's a good point. \
            A slightly more natural way to say that would be...'. \
            Your main goal is to help the user practice and improve their conversational English in a supportive way. \
            Keep your own responses clear and easy to understand.",
        }
    ]
# Inicializa a variável de estado para os bytes de áudio
if "audio_bytes_to_process" not in st.session_state:
    st.session_state.audio_bytes_to_process = None

# --- Layout da Interface ---

# --criar 2 colunas para o microfone e o botão de encerrar conversa
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### Gravar Mensagem de Voz")
    st.audio_input(
        "Grave sua mensagem de voz aqui:",
        key="audio_input_user",
        on_change=process_audio_callback,
    )

    # --- Lógica de Processamento ---
    # Verifica se o callback preparou bytes de áudio para processamento
    if st.session_state.audio_bytes_to_process:
        st.info("Processando seu áudio...")
        audio_bytes = st.session_state.audio_bytes_to_process

        # 1. Transcrever o áudio do usuário
        transcription = transcribe_audio(audio_bytes)

        if transcription and transcription.strip():
            st.session_state.mensagens.append(
                {"role": "user", "content": transcription}
            )

            # 2. Obter resposta do assistente
            with st.spinner("Pensando..."):
                text_answer_assistant = answer_assistant(st.session_state.mensagens)
                st.session_state.mensagens.append(
                    {"role": "assistant", "content": text_answer_assistant}
                )

            # 3. Gerar áudio da resposta
            with st.spinner("Gerando áudio da resposta..."):
                assistant_audio_bytes = make_audio_assistant(text_answer_assistant)
                if assistant_audio_bytes:
                    st.session_state.audio_to_play = assistant_audio_bytes
        else:
            st.warning("Não foi possível entender o áudio, por favor tente novamente.")

        # Limpa os bytes de áudio para não reprocessar na próxima execução
        st.session_state.audio_bytes_to_process = None
with col2:
    st.markdown("### Encerrar Conversa")
    st.markdown("Clique no botão abaixo para encerrar a conversa e limpar o histórico.")
    if st.button("Encerrar Conversa", use_container_width=True):
        st.session_state.clear()  # Limpa todo o estado da sessão
        st.rerun()

# --- Exibição do Chat ---
# Usamos um container como um "placeholder" para organizar o histórico da conversa.
st.header("Histórico da Conversa")

# Filtra apenas as mensagens de 'user' e 'assistant' para exibição
display_messages = [
    msg for msg in st.session_state.mensagens if msg["role"] != "system"
]

# Define a altura do container para adicionar uma barra de rolagem se houver muitas mensagens
container_height = 500 if len(display_messages) > 6 else None

chat_container = st.container(height=container_height)
with chat_container:
    # Itera sobre as mensagens em ordem inversa para mostrar a mais recente no topo
    for msg in display_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# --- Reprodução do Áudio do Assistente ---
# Esta parte é executada no final do script para garantir que a interface
# seja atualizada antes de o áudio começar a tocar.
if "audio_to_play" in st.session_state and st.session_state.audio_to_play:
    audio_bytes = st.session_state.audio_to_play
    st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    # Limpa a variável de estado para não tocar novamente.
    del st.session_state.audio_to_play

# --- Componente para auto-scroll ---
# Injeta JavaScript para rolar o container de chat para o final.
# Apenas se o container tiver altura fixa (e portanto, uma barra de rolagem).
if container_height:
    components.html(
        """
        <script>
            const scrollables = window.parent.document.querySelectorAll('div[data-testid="stContainer"] div[style*="overflow: auto"]');
            if (scrollables.length > 0) {
                const lastScrollable = scrollables[scrollables.length - 1];
                lastScrollable.scrollTop = lastScrollable.scrollHeight;
            }
        </script>
        """,
        height=0,
    )
