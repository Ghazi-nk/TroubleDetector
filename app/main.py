
import logging
import asyncio
import json
import threading
import time
from pathlib import Path


from openai_client import get_openai_client, get_response
from telegram_bot import send_message, start_polling  # You need to implement or mock this.

logging.basicConfig(level=logging.INFO)


async def main():
    try:
        # Load reports in JSON and turn them into a string
        report_path = Path("semgrep-service/reports/report.json")
        if not report_path.exists():
            raise FileNotFoundError(f"Report file not found: {report_path}")

        with report_path.open("r", encoding="utf-8") as f:
            report_json = json.load(f)
        semgrep_report_str = json.dumps(report_json, indent=2)


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
