from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from textgen.textGeneration import generateResponse
from textgen.firebaseDb import clear_history, getBalance


print('Starting up bot...')
TOKEN: Final = '6185686378:AAHrt6ldLSf7v8mArkmKM9OqhpF1iUwZ2Vk'
async def generate(username: str, message: str):

    response = await generateResponse(username, message);

    return response

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    firstname = update.message.from_user.first_name  # get user's first name
    text = f"""Reiko: *Every day, {firstname} has to deal with his older sister's clumsiness which causes many sexual accidents; today is also no exception.*
    *Reiko runs into {firstname} as she walks down the stairs.* "{firstname}-kun? Already back from scho-" *She trips over her feet and falls down at him.*"""

    clear_history(firstname);
    await update.message.reply_text(text)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name  # get user's first name
    text = f"Send your first message to begin the conversation!"
    await update.message.reply_text(text)

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username  # get user's first name
    balance = getBalance(username)
    # If user exists, fetch and display credits
    if balance>-10:
        await update.message.reply_text(f"Your current balance is: {balance} credits.")
    else:
        await update.message.reply_text("You don't have an account yet. Start chatting to create one!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    firstname = update.message.from_user.first_name  # get user's first name
    username = update.message.from_user.username
    balance = getBalance(username)

    if balance>0:
        response: str = await generate(firstname, text)
        await update.message.reply_text(response)
    else:
        await update.message.reply_text(f"Hello {firstname}, your balance is too low! Please top up your credits to continue.")

    # Print a log for debugging
    print(f'{firstname}: "{text}"')


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('balance', balance_command))
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)



