from typing import Final, List

import pandas as pd
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from textgen.textGeneration import generateResponse
from textgen.firebaseDb import clear_history


print('Starting up bot...')
TOKEN: Final = '6185686378:AAHrt6ldLSf7v8mArkmKM9OqhpF1iUwZ2Vk'
async def generate(username: str, message: str):

    response = await generateResponse(username, message);

    return response

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    firstname = update.message.from_user.first_name  # get user's first name
    text = f"""Reiko: *Every day, {firstname} has to deal with his older sister's clumsiness which causes many sexual accidents; today is also no exception.*
    *Reiko runs into Saul as she walks down the stairs.* "{firstname}-kun? Already back from scho-" *She trips over her feet and falls down at him.*"""

    clear_history(firstname);
    await update.message.reply_text(text)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name  # get user's first name
    text = f"Send your first message to begin the conversation!"
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

    response: str = await generate(user_name, text)
    await update.message.reply_text(response)

    # Print a log for debugging
    print(f'{user_name}: "{text}"')
    print(response)


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



