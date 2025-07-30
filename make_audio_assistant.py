import tempfile

from openai import APIError
from openai_client import client  # Supondo que você tenha um cliente OpenAI configurado

# --- Constantes ---
MODELO_GPT = "gpt-4"


# --- Constantes ---
SAMPLE_RATE = 16000  # Sample rate para a gravação de áudio
MODELO_WHISPER = "whisper-1"
MODELO_GPT = "gpt-4o"
MODELO_TTS = "tts-1"
VOZ_TTS = "onyx"


# ------------------
def make_audio_assistant(texto):
    """Gera o áudio a partir do texto e o salva em um arquivo temporário."""
    try:
        resposta = client.audio.speech.create(
            model=MODELO_TTS,
            voice=VOZ_TTS,
            input=texto,
        )
        # Usa um arquivo temporário para não poluir o diretório
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio_file:
            resposta.write_to_file(tmp_audio_file.name)
            return tmp_audio_file.name
    except APIError as e:
        print(f"Erro na API da OpenAI ao gerar áudio: {e}")
        return None
