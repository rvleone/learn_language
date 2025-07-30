import queue
import sys
import sounddevice as sd
import numpy as np


# --- Constantes ---
SAMPLE_RATE = 16000  # Sample rate para a gravação de áudio


def record_audio():
    """Grava o áudio do microfone até que a tecla Enter seja pressionada."""
    q = queue.Queue()

    def callback(indata, frames, time, status):
        """Função de callback chamada para cada bloco de áudio."""
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    print("Ouvindo... Pressione Enter para parar a gravação.")
    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE, channels=1, callback=callback, dtype="int16"
        ):
            input()  # Bloqueia até que Enter seja pressionado
    except Exception as e:
        print(f"Ocorreu um erro com o dispositivo de áudio: {e}")
        return np.array([], dtype="int16"), SAMPLE_RATE

    print("Gravação finalizada.")
    recording = (
        np.concatenate(list(q.queue)) if not q.empty() else np.array([], dtype="int16")
    )
    return recording, SAMPLE_RATE
