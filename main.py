from typing import Final, List

import pandas as pd
import requests
import json
import csv
# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')

TOKEN: Final = '6185686378:AAHrt6ldLSf7v8mArkmKM9OqhpF1iUwZ2Vk'
BOT_USERNAME: Final = '@lexi112_bot'

messageHist = ["jhjnhkn", "req", "res"]
oldMessageHist = ["hhhhk", "hjjhjjn", "hgjhbhj"]
def api_call(name: str, message: str):
    global messageHist
    global oldMessageHist

    url = "https://text-lexi-xbuls6ziyq-uc.a.run.app"

    payload = json.dumps({
        "name": name,
        "message": message,
        "history": messageHist
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response_data = response.json()

    oldMessageHist = messageHist.copy()
    messageHist = response_data.get('history', [])

    return response_data.get('message', '')
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name  # get user's first name
    text = f"Hey {user_name}!! I'm so excited to see you! The weather is great for a picnic, I brought some sushi, what did you bring?"
    global messageHist
    messageHist = ["Lexi:"+text]
    await update.message.reply_text(text)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name  # get user's first name
    text = f"Send your first message to lexi to begin the conversation!"
    global messageHist
    messageHist = []
    await update.message.reply_text(text)

def list_to_json_str(lst: List[str]) -> str:
    return json.dumps({"History": lst})
async def save_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global messageHist, oldMessageHist

    if len(messageHist) >= 2:
        data = {
            'messageHist': [list_to_json_str(oldMessageHist)],
            'request': [messageHist[-2]],
            'response': [messageHist[-1]]
        }
        df = pd.DataFrame(data)
        df.to_csv('conversation_history.csv', mode='a', index=False, header=False)
    else:
        print("Error saving, Not enough messages.")

    await update.message.reply_text("Conversation saved!")



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global messageHist

    text: str = update.message.text
    user_name = update.message.from_user.first_name  # get user's first name
    if (len(messageHist) == 0):
        messageHist = [f"{user_name}: " + text]

    response: str = api_call(user_name, text)
    await update.message.reply_text(response)

    # Print a log for debugging
    print(f'{user_name}: "{text}"')
    print('Lexi:', response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('save', save_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)



