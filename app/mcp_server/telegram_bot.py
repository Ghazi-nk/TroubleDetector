import asyncio

import json
import logging
import os

import threading
import time

import openai

import telebot
from dotenv import load_dotenv

from telegram.constants import ParseMode

# Load environment variables from .env file
load_dotenv(dotenv_path="../../.env")

BOT_TOKEN = os.getenv('BOT_TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')

# Creates a bot instance and passed the BOT_TOKEN to it
bot = telebot.TeleBot(BOT_TOKEN)

# Initialize OpenAI client if necessary
client = openai.OpenAI(api_key=openai.api_key)


# create empty user object
# user = get_empty_user()
# user: User





# Message handler that handles incoming '/start' and '/hello'
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    try:
        bot.send_message(message.chat.id, "Welcome!")
        # Create a new thread for the user

        #todo: logic when starting convo
    except Exception as e:
        logging.error(f"Failed to send welcome message: {e}")


def fetch_json():
    pardir_path = os.path.abspath(os.pardir)
    file_path = os.path.join(pardir_path, 'FE', 'output.json')
    logging.info(f"Fetching JSON from {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            flats_data = json.load(file)
            logging.info("Successfully fetched JSON data.")
            return flats_data
    except FileNotFoundError:
        logging.info(f"File {file_path} not found.")
        return []
    except json.decoder.JSONDecodeError:
        logging.info(f"Error decoding JSON from file {file_path}.")
        return []


# handle main use_case
def notify_user():
    try:
        response = "response"
        bot.send_message("user ID", response) # todo: heres how to send message to user
    except Exception as e:
        logging.error(f"Failed to notify user: {e}")


# Handler method for all other text messages
@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    user_id = message.from_user.id
    logging.info(f"Received message from user ID: {user_id}")


    # Retrieve or create a new thread_id for the user
    thread_id = message.chat.id
    if not thread_id:
        send_welcome(message)
        return

    response = "response string"
    text = escape_characters(response.text.replace('**', '*').replace('"', ''), '_>~`#+-=|{}.!')

    bot.send_message(chat_id=message.chat.id, text=text.replace('\\n', '\\\n'), parse_mode=ParseMode.MARKDOWN_V2)


def escape_characters(text, characters_to_escape):
    escaped_text = ""
    for char in text:
        if char in characters_to_escape:
            escaped_text += '\\' + char
        else:
            escaped_text += char
    return escaped_text


def start_polling():
    while True:
        try:
            asyncio.run(bot.polling(non_stop=True, interval=1, timeout=0))
        except:
            time.sleep(5)


# Start polling for messages
if __name__ == "__main__":
    bot_thread = None
    schedule_thread = None
    try:
        # Bot's polling in a thread
        bot_thread = threading.Thread(target=start_polling)
        logging.info(f"Starting polling thread: {bot_thread}")
        bot_thread.start()

        # Keep the main thread alive
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
        if bot_thread is not None: bot_thread.join()
        if schedule_thread is not None: schedule_thread.join()
