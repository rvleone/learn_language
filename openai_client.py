from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# Carrega as variáveis de ambiente do arquivo .env
_ = load_dotenv(find_dotenv())

client = OpenAI()
