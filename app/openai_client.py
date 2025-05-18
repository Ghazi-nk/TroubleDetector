# openai_client.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file if needed
# load_dotenv("app/.env")

def get_openai_client(api_key=None, model="gpt-4"):
    """Initializes and returns an OpenAI client instance."""
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    print(f"[DEBUG] Using API Key: {api_key}")
    if not api_key:
        raise ValueError("OpenAI API key must be set via argument or environment variable.")
    client = OpenAI(api_key=api_key)
    return client, model

def get_response(prompt: str, client, model="gpt-4") -> str:
    """Sends a prompt to the OpenAI API and returns the assistant's response."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error during OpenAI request: {e}"

if __name__ == "__main__":
    client, model = get_openai_client()
    test_prompt = "Summarize the main points of the Agile methodology."
    print(get_response(test_prompt, client, model))
