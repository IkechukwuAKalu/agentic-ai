import os

from dotenv import load_dotenv
from enum import Enum
from openai import OpenAI

load_dotenv(override = True)

# Replace the base URL with that of OpenAI if you are using a direct integration
OPENAI_BASE_URL = "https://openai.vocareum.com/v1"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class OpenAIModels(str, Enum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_41_MINI = "gpt-4.1-mini"
    GPT_41_NANO = "gpt-4.1-nano"


def openai_client(): return OpenAI(base_url = OPENAI_BASE_URL, api_key = OPENAI_API_KEY)