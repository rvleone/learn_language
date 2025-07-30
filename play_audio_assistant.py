from pathlib import Path
from playsound import playsound


def play_audio_assistant(path_audio):
    """Reproduz um arquivo de áudio e o remove em seguida."""
    try:
        playsound(path_audio)
    finally:
        Path(path_audio).unlink()  # Garante a remoção do arquivo temporário
