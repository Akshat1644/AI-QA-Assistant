import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# -----------------------------
# Multiple API Keys
# -----------------------------

API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
]

API_KEYS = [key for key in API_KEYS if key]

# -----------------------------
# Models (Fast → Lite → Pro)
# -----------------------------

MODELS = [
    "gemini-2.5-flash"
]


def generate_ai_response(prompt):

    last_error = None

    # Try every API key
    for api_key in API_KEYS:

        client = genai.Client(api_key=api_key)

        # For every key, try every model
        for model in MODELS:

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if response.text:
                    return response.text

            except Exception as e:

                print(f"[API] {api_key[:8]}... | {model} failed -> {e}")

                last_error = e

                continue

    raise Exception(
        f"All Gemini API Keys and Models failed.\n{last_error}"
    )