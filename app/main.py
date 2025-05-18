import logging
import asyncio
from openai_client import get_openai_client, get_response

logging.basicConfig(level=logging.INFO)

async def main():
    try:
        # load reports in json and turn them into string from app/semgrep-service/reports/report.json

        # create prompt using build_promt

        # send prompt to openai and get response

        # start the bot

        # push response to telegram bot



        prompt = "this is a test. just say hey!"

        #client, model = get_openai_client()
        #response = get_response(prompt, client, model)
        response = "This is a mock response for testing."
        logging.info(f"OpenAI response: {response}")
    except Exception as e:
        logging.error(f"Error in main process: {e}")



def build_prompt(prompt: str, semgrep_report: str) -> str:
    """
    Builds the prompt for OpenAI API.
    """
    return f"{prompt}\n{semgrep_report}"

if __name__ == "__main__":
    asyncio.run(main())
