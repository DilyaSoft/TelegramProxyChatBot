from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHATGPT_API_KEY = os.getenv('CHATGPT_API_KEY')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Send me a message and I will forward it to ChatGPT.')

def echo(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = requests.post(
        'https://api.openai.com/v1/engines/gpt-4/chat/completions',
        headers={'Authorization': f'Bearer {CHATGPT_API_KEY}'},
        json={
            'messages': [
                {'role': 'user', 'content': user_message}
            ]
        }
    )
    chatgpt_response = response.json()
    reply_message = chatgpt_response['choices'][0]['message']['content']
    update.message.reply_text(reply_message)

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
