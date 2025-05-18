# openai_client.py

import os
from openai import OpenAI
from dotenv import load_dotenv  # Correct import for dotenv

# Load environment variables from the .env file
load_dotenv("app/.env")

class OpenAIClient:
    def __init__(self, api_key=None, model="gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        print(f"[DEBUG] Using API Key: {self.api_key}")
        if not self.api_key:
            raise ValueError("OpenAI API key must be set via argument or environment variable.")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def get_response(self, prompt: str) -> str:
        """Sends a prompt to the OpenAI API and returns the assistant's response."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},#todo: improve system prompt
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error during OpenAI request: {e}"

if __name__ == "__main__":
    client = OpenAIClient()
    test_prompt = "Summarize the main points of the Agile methodology."
    print(client.get_response(test_prompt))
