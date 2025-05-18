
import logging
import asyncio
import json
import threading
import time


from app.github_client import retrieve_repo
from openai_client import get_openai_client, get_response
from telegram_bot import send_message, start_polling  # You need to implement or mock this.
from semgrep_client import get_semgrep_report  # You need to implement or mock this.

logging.basicConfig(level=logging.INFO)

def handle_repo_name(repo_name, chat_id):
    """
    Handle the GitHub repository name.
    This function should implement the logic to use the repo name.
    """
    # Implement your logic here
    logging.info(f"Handling repository name: {repo_name}")
    # retrieve repos from github
    retrieve_repo(repo_name)
    # use semgrep to analyze the repo and generate a report
    semgrep_report_str = get_semgrep_report()
    # create a output out of the report using openai
    client, model = get_openai_client()
    response = get_response(semgrep_report_str, client, model)
    # send the output to the user
    send_message(chat_id, response)




async def main():
    try:
        # Load reports in JSON and turn them into a string

        semgrep_report_str = get_semgrep_report()

        # Send prompt to OpenAI and get response
        client, model = get_openai_client()
        response = get_response(semgrep_report_str, client, model)


        logging.info("Telegram Bot pooling started")
        thread = threading.Thread(target=start_polling)
        logging.info("Starting Telegram bot polling...")
        thread.start()

        # Push response to Telegram bot
        user_id = 1016498662  # Replace with actual user ID
        logging.info(f"Sending response to user. Response: {response}")
        send_message(user_id, response)


        logging.info(f"OpenAI response successfully sent to Telegram: {response}")
        while True:
            time.sleep(10)

    except Exception as e:
        logging.error(f"Error in main process: {e}")


if __name__ == "__main__":
    asyncio.run(main())
