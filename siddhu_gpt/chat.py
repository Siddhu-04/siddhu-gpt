import os
from openai import OpenAI

GROQ_BASE   = "https://api.groq.com/openai/v1"
OLLAMA_BASE = "http://localhost:11434/v1"

MODELS = {
    "groq":   "llama-3.3-70b-versatile",
    "ollama": "llama3.2:3b",
}

def get_client(provider: str = "groq") -> OpenAI:
    if provider == "groq":
        return OpenAI(base_url=GROQ_BASE, api_key=os.getenv("GROQ_API_KEY"))
    if provider == "ollama":
        return OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    raise ValueError(f"Unknown provider: {provider}")

def list_providers() -> list[str]:
    providers = []
    if os.getenv("GROQ_API_KEY"):
        providers.append("groq")
    # ollama is local, always available if running
    providers.append("ollama")
    return providers

def pick_model(provider: str) -> str:
    return MODELS.get(provider, "llama-3.3-70b-versatile")

def chat_once(client, messages: list[dict], model: str) -> str:
    resp = client.chat.completions.create(model=model, messages=messages)
    return resp.choices[0].message.content

def chat_stream(client, messages: list[dict], model: str):
    stream = client.chat.completions.create(
        model=model, messages=messages, stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content