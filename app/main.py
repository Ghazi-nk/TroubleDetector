
import logging
import asyncio

import threading
import time
from pathlib import Path

from openai_client import get_openai_client, get_response
from telegram_bot import send_message, start_polling
from semgrep_client import get_semgrep_report

logging.basicConfig(level=logging.INFO)





async def main():
    try:
        # Load reports in JSON and turn them into a string
        semgrep_report_str = get_semgrep_report(Path("app/semgrep-service/reports/report.json"))

        # Send prompt to OpenAI and get response
        client, model = get_openai_client()
        response = get_response(semgrep_report_str, client, model)

        # Start polling for Telegram bot
        logging.info("Telegram Bot pooling started")
        thread = threading.Thread(target=start_polling)
        logging.info("Starting Telegram bot polling...")
        thread.start()

        # Push response to Telegram bot admin
        user_id = 1016498662
        logging.info(f"Sending response to user. Response: {response}")
        send_message(user_id, response)


        logging.info(f"OpenAI response successfully sent to Telegram: {response}")
        while True:
            time.sleep(10)

    except Exception as e:
        logging.error(f"Error in main process: {e}")


if __name__ == "__main__":
    asyncio.run(main())
