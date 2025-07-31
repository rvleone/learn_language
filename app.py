import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components

# Importar as funções de processamento
from st_audio_recorder import start_recording, stop_recording
from answer_assistant import answer_assistant
from make_audio_assistant import make_audio_assistant
from transcribe_audio import transcribe_audio

# --- Configuração da Página ---
st.set_page_config(page_title="English Conversation Practice", layout="wide")
st.title("Pratique a sua conversação em inglês")
st.markdown(
    "Bem vindo! para praticar a sua conversação em inglês, basta clicar no botão Gravar Áudio, falar e depois clicar em Parar Gravação."
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
if "is_recording" not in st.session_state:
    st.session_state.is_recording = False

# --- Layout da Interface ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button(
        "Gravar Áudio",
        on_click=start_recording,
        disabled=st.session_state.is_recording,
        use_container_width=True,
    ):
        st.rerun()

with col2:
    if st.button(
        "Parar Gravação",
        disabled=not st.session_state.is_recording,
        use_container_width=True,
    ):
        audio_data, sample_rate = stop_recording()

        if audio_data.size > 0:
            st.info("Processando seu áudio...")

            # 1. Transcrever o áudio do usuário
            transcription = transcribe_audio(audio_data, sample_rate)

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
                st.warning(
                    "Não foi possível entender o áudio, por favor tente novamente."
                )
        else:
            st.warning("Nenhum áudio foi gravado.")

        st.rerun()

with col3:
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
