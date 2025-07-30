from dotenv import load_dotenv, find_dotenv
import streamlit as st
from openai import OpenAI

# Carrega as variáveis de ambiente do arquivo .env
_ = load_dotenv(find_dotenv())

try:
    client = OpenAI()
except Exception as e:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
