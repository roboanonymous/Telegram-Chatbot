import logging

from flask import Flask, request
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,CallbackContext, Dispatcher
from telegram import Update,Bot
from Dialog import get_reply, fetch_news,  topics_keyboard

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger=logging.getLogger(__name__)
 
 # telegram bot token
TOKEN = "1952355515:AAEvqbSRsrt2xrbugWTqJ2kxqqkFSBovjXM"

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello!"


@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    """webhook view which receives updates from telegram"""
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "ok"


def echo_text(bot,update):
    reply=update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=reply)


def reply_text(update: Update,context: CallbackContext):
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent == "get_news":
        articles = fetch_news(reply)
        for article in articles:
            bot.send_message(chat_id=update.message.chat_id, text=article['link'])
    else:
        bot.send_message(chat_id=update.message.chat_id, text=reply)

def echo_sticker(bot,update):
   """callback function for sticker message handler"""
    bot.send_sticker(chat_id=update.message.chat_id , sticker=update.message.sticker.file_id)



def news(update: Update,context: CallbackContext):
    """callback function for /news handler"""
    bot.send_message(chat_id=update.message.chat_id, text="Choose a category",
                     reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))


def error(bot,update):
    """callback function for error handler"""
    logger.error("Update '%s' has caused error '%s", update, update.error)

def greeting(update: Update,context: CallbackContext):
   """callback function for /start handler"""
    first_name = update.to_dict()['message']['chat']['first_name']
    update.message.reply_text("hi {}".format(first_name))

"""def message_handler(update: Update,context: CallbackContext):
    text = update.to_dict()['message']['text']
    update.message.reply_text(text)"""

if __name__=="__main__":


    bot = Bot(TOKEN)
    bot.set_webhook("https://0ce3c8a12cfa.ngrok.io/" + TOKEN)

    dp = Dispatcher(bot, None)
    dp.add_handler(CommandHandler("start" , greeting))
    dp.add_handler(CommandHandler("help" , help))
    dp.add_handler(MessageHandler(Filters.text ,  reply_text))
    dp.add_handler(CommandHandler("news", news))
    dp.add_handler(MessageHandler(Filters.sticker ,echo_sticker))
    dp.add_error_handler(error)


    app.run(port=8443)

