import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


def load_openai_environment():
    base_dir = Path(__file__).resolve().parents[1]
    candidates = [
        base_dir.parent / 'openAI.env',
        base_dir.parent.parent / 'openAI.env',
    ]
    for env_path in candidates:
        if env_path.exists():
            load_dotenv(env_path)
            break


def get_openai_api_key():
    load_openai_environment()
    return os.environ.get('openai_apikey') or os.environ.get('openai_api_key')


def get_openai_client():
    api_key = get_openai_api_key()
    if not api_key:
        raise RuntimeError(
            "OpenAI API key not found. Add 'openai_apikey=...' to openAI.env."
        )
    return OpenAI(api_key=api_key)
