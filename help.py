import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)
import choiceshidden as choice
import safetychoiceshidden as safec
import servicechoiceshidden as serec 
import os
PORT = int(os.environ.get('PORT', 5000))
TOKEN = '<TELEGRAM BOT TOKEN>'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

FIRST, SECOND = range(2)


def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    keyboard = [
            [InlineKeyboardButton("Safety", callback_data="Safety")],
            [InlineKeyboardButton("Service", callback_data="Service")],
            [InlineKeyboardButton("Communications", callback_data="Communications")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text="Hello, what can I do for you today?", reply_markup=reply_markup)
    return FIRST


def start_over(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
            [InlineKeyboardButton("Safety", callback_data="Safety")],
            [InlineKeyboardButton("Service", callback_data="Service")],
            [InlineKeyboardButton("Communications", callback_data="Communications")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="What else can I do for you today?", reply_markup=reply_markup)
    return FIRST


def end(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Press /start to restart the bot! See you again!")
    return ConversationHandler.END


def main() -> None:
    print('Bot Running')
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(choice.safety, pattern='^Safety$'),
                CallbackQueryHandler(choice.service, pattern='^Service$'),
                CallbackQueryHandler(choice.communications, pattern='^Communications$'),

                #Safety
                CallbackQueryHandler(safec.SafetyMission, pattern='^Safety Mission$'),
                CallbackQueryHandler(safec.SafetyTheme, pattern='^Safety Theme$'),


                CallbackQueryHandler(start_over, pattern='^Start Over$'),
                CallbackQueryHandler(end, pattern='^End$'),
            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern='^Start Over$'),
                CallbackQueryHandler(end, pattern='^End$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook(''https://<appname>.herokuapp.com/'' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
