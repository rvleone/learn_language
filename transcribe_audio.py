import io
import streamlit as st
from openai import APIError
from openai_client import client
import numpy as np
from scipy.io.wavfile import write as write_wav

# --- Constantes ---
MODELO_WHISPER = "whisper-1"


def transcribe_audio(audio_data: np.ndarray, sample_rate: int) -> str:
    """Converte o áudio gravado (numpy array) para texto usando a API da OpenAI."""
    try:
        # Cria um arquivo WAV em memória a partir do array numpy
        wav_bytes = io.BytesIO()
        write_wav(wav_bytes, sample_rate, audio_data)
        wav_bytes.seek(0)
        wav_bytes.name = "audio.wav"  # A API precisa de um nome de arquivo

        # A API do OpenAI pode receber um objeto file-like.
        transcricao = client.audio.transcriptions.create(
            model=MODELO_WHISPER, file=wav_bytes, language="en"
        )
        return transcricao.text
    except APIError as e:
        st.error(f"Erro na API da OpenAI ao transcrever o áudio: {e}")
        return ""
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o áudio: {e}")
        return ""
