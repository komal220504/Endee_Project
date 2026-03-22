import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Use Ollama's OpenAI-compatible endpoint
ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
ollama_model = os.getenv("OLLAMA_MODEL", "llama2")

# Check if Ollama is available
def is_ollama_available():
    """Check if Ollama server is running."""
    try:
        response = requests.get(
            ollama_url.replace("/v1", "") + "/api/tags",
            timeout=2
        )
        return response.status_code == 200
    except (requests.RequestException, Exception):
        return False

# Initialize client - try OpenAI first, fallback to direct HTTP
client = None
ollama_available = is_ollama_available()
use_direct_api = False

if ollama_available:
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key="ollama",  # Ollama doesn't require API key
            base_url=ollama_url
        )
    except Exception as e:
        print(f"Warning: OpenAI library initialization failed: {e}")
        print("Using direct Ollama API instead")
        use_direct_api = True


def generate_answer(query, docs):
    context = "\n".join(docs).strip()
    if not context:
        return "No context provided"

    if not ollama_available:
        return f"LLM not available: Ollama server is not running at {ollama_url}. Please install and start Ollama from https://ollama.ai"

    prompt = f"""Answer using context only

Question: {query}

Context:
{context}
"""

    try:
        if use_direct_api:
            # Use direct Ollama API
            ollama_api_url = ollama_url.replace("/v1", "") + "/api/generate"
            payload = {
                "model": ollama_model,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(ollama_api_url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "No response from Ollama").strip()
        else:
            # Use OpenAI client
            r = client.chat.completions.create(
                model=ollama_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Answer questions based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            if hasattr(r, "choices") and r.choices:
                return r.choices[0].message.content.strip()

            return "No response"
    except Exception as e:
        return f"LLM Error: {str(e)}. Make sure Ollama is running: ollama serve"