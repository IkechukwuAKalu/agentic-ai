from enum import Enum
from openai import OpenAI

OLLAMA_BASE_URL = "http://localhost:11434/v1"
OLLAMA_API_KEY = "ollama"


class OllamaModels(str, Enum):
    LLAMA_32 = "llama3.2"


def ollama_client(): return OpenAI(base_url = OLLAMA_BASE_URL, api_key = OLLAMA_API_KEY)