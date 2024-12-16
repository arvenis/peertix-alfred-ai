import logging
from os import getenv
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = getenv("LOG_LEVEL", logging.INFO)


IMAGE_NAME = getenv("IMAGE_NAME", "pt-alfred-ai:dev")


class SecretConfig:
    GROUP = getenv("SECRET_GROUP", "flyte-secrets")  # The name of the secret in the cluster
    FIREBASE = getenv("FIREBASE_SECRET_NAME", "firebase-credentials")
    SERPER = getenv("SERPER_SECRET_NAME", "serper-api-key")
    SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID_SECRET_NAME", "spotify-client-id")
    SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET_NAME", "spotify-client-secret")
    GEMINI = getenv("GEMINI_SECRET_NAME", "gemini-api-key")


ENVS = {
    "OPENAI_MODEL_NAME": getenv("OPENAI_MODEL_NAME"),
    "OPENAI_API_KEY": getenv("OPENAI_API_KEY"),
    "SERPER_API_KEY": getenv("SERPER_API_KEY"),
    "SPOTIFY_CLIENT_ID": getenv("SPOTIFY_CLIENT_ID"),
    "SPOTIFY_CLIENT_SECRET": getenv("SPOTIFY_CLIENT_SECRET"),
    "GEMINI_API_KEY": getenv("GEMINI_API_KEY"),
}
