import queue
import sys

import numpy as np
import sounddevice as sd
import streamlit as st

# --- Constantes ---
SAMPLE_RATE = 16000  # Sample rate para a gravação de áudio


def start_recording():
    """Inicia a gravação de áudio e armazena o stream e a fila no st.session_state."""
    if "is_recording" not in st.session_state:
        st.session_state.is_recording = False

    if st.session_state.is_recording:
        return  # Já está gravando

    # Cria uma nova fila para cada gravação para não acumular áudio antigo.
    st.session_state.audio_queue = queue.Queue()

    q = st.session_state.audio_queue

    def callback(indata, frames, time, status):
        """Função de callback chamada para cada bloco de áudio."""
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    try:
        stream = sd.InputStream(
            samplerate=SAMPLE_RATE, channels=1, dtype="int16", callback=callback
        )
        stream.start()
        st.session_state.audio_stream = stream
        st.session_state.is_recording = True
    except Exception as e:
        st.error(f"Ocorreu um erro com o dispositivo de áudio: {e}")
        st.session_state.is_recording = False


def stop_recording():
    """Para a gravação, processa os dados e os retorna."""
    if "is_recording" not in st.session_state or not st.session_state.is_recording:
        return np.array([], dtype="int16"), SAMPLE_RATE

    if "audio_stream" in st.session_state and st.session_state.audio_stream:
        stream = st.session_state.audio_stream
        stream.stop()
        stream.close()
        del st.session_state.audio_stream

        q = st.session_state.audio_queue
        recording = (
            np.concatenate(list(q.queue))
            if not q.empty()
            else np.array([], dtype="int16")
        )
        st.session_state.is_recording = False
        return recording, SAMPLE_RATE

    st.session_state.is_recording = False
    return np.array([], dtype="int16"), SAMPLE_RATE
