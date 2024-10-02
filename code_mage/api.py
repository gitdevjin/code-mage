import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
import toml
from .loadConfig import load_config

def call_api(model, target_lang, code, stream_flag = False):
    supported_model = ["groq", "openrouter"]

    # Default config in case the file does not exist
    config = load_config()
        
    # Default model is openrouter
    api_url = "https://openrouter.ai/api/v1"
    api_key = os.getenv("OPENROUTER_API_KEY") or config.get('OPENROUTER_API_KEY')
    api_model = "sao10k/l3-euryale-70b"

    # Varify Model, and then Set API_URL and API_KEY
    if model == "groq":
        api_url = "https://api.groq.com/openai/v1"
        api_key = os.getenv("GROQ_API_KEY") or config.get('GROQ_API_KEY')
        api_model = "llama3-8b-8192"
    elif model is not None and model not in supported_model:
        sys.exit(f"{model} api model is not suppored. Model Supported: f{supported_model}")
        
    client = OpenAI(
        base_url = api_url,
        api_key = api_key,
    )

    completion = client.chat.completions.create(
        extra_headers={
            },
        model=api_model,
        messages=[
            {"role": "system", "content": "only display the code without any explanation"},
            {"role": "user", "content": f"translate this to {target_lang} language: {code}"},
        ],
        stream=stream_flag,
    )

    return completion