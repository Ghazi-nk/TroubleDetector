import os
import logging
import threading
import time

import telebot
from dotenv import load_dotenv
from telegram.constants import ParseMode



# Load environment variables from .env
load_dotenv(".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing from environment.")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing from environment.")

bot = telebot.TeleBot(BOT_TOKEN)


logging.basicConfig(level=logging.INFO)

def escape_characters(text, characters_to_escape):
    escaped_text = ""
    for char in text:
        if char in characters_to_escape:
            escaped_text += '\\' + char
        else:
            escaped_text += char
    return escaped_text

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome! Send me a prompt followed by your sonar report.")

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    user_input = message.text.strip()
    chat_id = message.chat.id

    # For demo purposes, assume split by a line break into prompt and sonar_report
    if "\n" not in user_input:
        bot.send_message(chat_id, "Please provide input in the format:\n<Prompt>\\n<Your Sonar Report>")
        return

    try:
        prompt, sonar_report = user_input.split("\n", 1)
        bot.send_message(chat_id, "Thinking...")
        response = "static response"

        # Escape characters for Telegram MarkdownV2
        characters_to_escape = '_>~`#+-=|{}.!'
        safe_text = escape_characters(response, characters_to_escape)

        bot.send_message(chat_id, safe_text, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        bot.send_message(chat_id, "Something went wrong while processing your request.")

def start_polling():
    while True:
        try:
            bot.polling(non_stop=True, interval=1, timeout=0)
        except Exception as e:
            logging.error(f"Polling error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    thread = threading.Thread(target=start_polling)
    logging.info("Starting Telegram bot polling...")
    thread.start()

    while True:
        time.sleep(10)
