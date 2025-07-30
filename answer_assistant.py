from openai import APIError
from openai_client import client

# --- Constantes ---
MODELO_GPT = "gpt-4"


def answer_assistant(mensagens):
    """Envia a conversa para a API da OpenAI e retorna a resposta do assistente."""
    try:
        resposta = client.chat.completions.create(
            messages=mensagens,
            model=MODELO_GPT,
            max_tokens=1000,
            temperature=0,
        )
        return resposta.choices[0].message.content or ""
    except APIError as e:
        print(f"Erro na API da OpenAI ao gerar texto: {e}")
        return "Desculpe, ocorreu um erro e não consigo responder agora."
