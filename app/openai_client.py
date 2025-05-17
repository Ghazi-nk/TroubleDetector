# openai_client.py

import openai
import os

class OpenAIClient:
    def __init__(self, api_key=None, model="gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be set via argument or environment variable.")
        self.model = model
        openai.api_key = self.api_key

    def get_ai_response(self, prompt: str, sonar_report: str) -> str:
        """Combines prompt and sonar_report, sends to OpenAI API, and returns the response."""
        full_prompt = f"{prompt}\n\nSonar Report:\n{sonar_report}"

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},#todo: optimize this
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message["content"].strip()
        except Exception as e:
            return f"Error during OpenAI request: {e}"

if __name__ == "__main__":
    # For testing purposes
    client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Analyze the following sonar report."
    sonar_report = "Sonar report data goes here."
    response = client.get_ai_response(prompt, sonar_report)
    print(response)