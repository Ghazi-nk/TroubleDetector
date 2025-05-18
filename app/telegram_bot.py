import os
import logging
import threading
import time

import telebot
from dotenv import load_dotenv

# Suggest commands (users see this when typing '/')
from telebot import types
from telegram.constants import ParseMode

from app.github_client import retrieve_repo
from app.openai_client import get_openai_client, get_response
from app.semgrep_client import get_semgrep_report

# Load environment variables from .env
load_dotenv(".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing from environment.")

bot = telebot.TeleBot(BOT_TOKEN)

bot.set_my_commands([
    types.BotCommand("start", "Start the bot"),
    types.BotCommand("githubrepo", "Submit a GitHub repository name")
])

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

@bot.message_handler(commands=['GithubRepo'])
def github_repo_handler(message):
    msg = bot.send_message(
        message.chat.id,
        "Please enter the full GitHub repository name (e.g., `owner/repo`):",
        parse_mode=ParseMode.MARKDOWN
    )

    bot.register_next_step_handler(msg, lambda msg2: (
        bot.send_message(msg2.chat.id, "❌ Invalid format. Please use `owner/repo` format.")
        if '/' not in msg2.text.strip() or len(msg2.text.strip().split('/')) != 2
        else (
            bot.send_message(msg2.chat.id, f"✅ Repository name received: `{msg2.text.strip()}`", parse_mode=ParseMode.MARKDOWN),
            handle_repo_name(msg2.text.strip(), msg2.chat.id)
        )
    ))


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
    logging.info(f"Response sent to user: {response}")



if __name__ == "__main__":
    thread = threading.Thread(target=start_polling)
    logging.info("Starting Telegram bot polling...")
    thread.start()
    while True:
        time.sleep(10)