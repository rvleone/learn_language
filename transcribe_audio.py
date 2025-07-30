from io import BytesIO

from scipy.io.wavfile import write as write_wav

from openai import APIError
from openai_client import client

# --- Constantes ---
MODELO_WHISPER = "whisper-1"


def transcribe_audio(audio_data, sample_rate):
    """Converte o áudio gravado para texto usando a API da OpenAI."""
    wav_data = BytesIO()
    write_wav(wav_data, sample_rate, audio_data)
    wav_data.seek(0)
    wav_data.name = "audio.wav"
    try:
        transcricao = client.audio.transcriptions.create(
            model=MODELO_WHISPER, file=wav_data, language="en"
        )
        return transcricao.text
    except APIError as e:
        print(f"Erro na API da OpenAI ao transcrever o áudio: {e}")
        return ""
