import io
import streamlit as st
from openai import APIError
from openai_client import client

# --- Constantes ---
MODELO_WHISPER = "whisper-1"


def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcreve um áudio em bytes usando a API Whisper da OpenAI."""
    try:
        # Cria um objeto file-like em memória a partir dos bytes do áudio.
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.wav"  # A API precisa de um nome para inferir o tipo.

        transcricao = client.audio.transcriptions.create(
            model=MODELO_WHISPER, file=audio_file, language="en"
        )
        return transcricao.text
    except APIError as e:
        st.error(f"Erro na API da OpenAI ao transcrever o áudio: {e}")
        return ""
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o áudio: {e}")
        return ""
