from os import getenv
from dotenv import load_dotenv

load_dotenv()


ENVS = {
    "OPENAI_MODEL_NAME": getenv("OPENAI_MODEL_NAME"),
    "OPENAI_API_KEY": getenv("OPENAI_API_KEY"),
    "SERPER_API_KEY": getenv("SERPER_API_KEY"),
    "SPOTIFY_CLIENT_ID": getenv("SPOTIFY_CLIENT_ID"),
    "SPOTIFY_CLIENT_SECRET": getenv("SPOTIFY_CLIENT_SECRET"),
    "GEMINI_API_KEY": getenv("GEMINI_API_KEY"),
}