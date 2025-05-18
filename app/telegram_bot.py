import os
import logging
import threading
import time

import telebot
from dotenv import load_dotenv



# Load environment variables from .env
load_dotenv(".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing from environment.")

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



def send_message(chat_id, response):
    """
    Send a message to the Telegram bot.
    """
    try:
        bot.send_message(chat_id, response)
    except Exception as e:
        logging.error(f"Error sending message to Telegram: {e}")
        raise

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