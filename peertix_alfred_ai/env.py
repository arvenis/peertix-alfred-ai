import logging
from os import getenv
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = getenv("LOG_LEVEL", logging.INFO)


class FirebaseConfig:
    SECRET_GROUP = getenv("FIREBASE_SECRET_GROUP", "firebase-credentials")
    SECRET_NAME = getenv("FIREBASE_SECRET_NAME", "firebase-credentials")


ENVS = {
    "OPENAI_MODEL_NAME": getenv("OPENAI_MODEL_NAME"),
    "OPENAI_API_KEY": getenv("OPENAI_API_KEY"),
    "SERPER_API_KEY": getenv("SERPER_API_KEY"),
    "SPOTIFY_CLIENT_ID": getenv("SPOTIFY_CLIENT_ID"),
    "SPOTIFY_CLIENT_SECRET": getenv("SPOTIFY_CLIENT_SECRET"),
    "GEMINI_API_KEY": getenv("GEMINI_API_KEY"),
}
