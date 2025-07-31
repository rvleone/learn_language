from openai import APIError
from openai_client import client  # Supondo que você tenha um cliente OpenAI configurado


# --- Constantes ---
MODELO_TTS = "tts-1"
VOZ_TTS = "onyx"


# ------------------
def make_audio_assistant(texto):
    """Gera o áudio a partir do texto e retorna os bytes."""
    try:
        resposta = client.audio.speech.create(
            model=MODELO_TTS,
            voice=VOZ_TTS,
            input=texto,
        )
        return resposta.content
    except APIError as e:
        print(f"Erro na API da OpenAI ao gerar áudio: {e}")
        return None
