from record_audio import record_audio
from transcribe_audio import transcribe_audio
from answer_assistant import answer_assistant
from make_audio_assistant import make_audio_assistant
from play_audio_assistant import play_audio_assistant


if __name__ == "__main__":

    mensagens = [
        {
            "role": "system",
            "content": "You are a helpful and friendly assistant for practicing English conversation. Keep your answers concise and clear.",
        }
    ]

    while True:
        audio_data, sample_rate = record_audio()
        if audio_data.size == 0:
            print("Nenhum áudio foi gravado. Tente novamente.")
            continue

        transcribe = transcribe_audio(audio_data, sample_rate)
        if not transcribe.strip():
            print("Não foi possível entender o áudio, tente novamente.")
            continue

        print(f"User: {transcribe}")

        if transcribe.strip().lower() in ["exit", "quit", "sair"]:
            print("Encerrando a conversa. Até mais!")
            break

        mensagens.append({"role": "user", "content": transcribe})
        text_answer_assistant = answer_assistant(mensagens)
        mensagens.append({"role": "assistant", "content": text_answer_assistant})
        print(f"Assistant: {text_answer_assistant}")
        temp_path_audio = make_audio_assistant(text_answer_assistant)
        if temp_path_audio:
            play_audio_assistant(temp_path_audio)
