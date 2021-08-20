import logging
from flask import Flask, request
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,CallbackContext, Dispatcher
from telegram import Update,Bot


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger=logging.getLogger(__name__)
 
TOKEN = "xxx2355515:AAEvqbSRsrt2xrbugWTqJ2kxqqkFSBovjXM"

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello!"


@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
   
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "ok"

def echo_text(bot,update):
    reply=update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=reply)

def echo_sticker(bot,update):
    bot.send_sticker(chat_id=update.message.chat_id , sticker=update.message.sticker.file_id)

def error(bot,update):
    logger.error("Update '%s' has caused error '%s", update, update.error)

def greeting(update: Update,context: CallbackContext):
    first_name = update.to_dict()['message']['chat']['first_name']
    update.message.reply_text("hi {}".format(first_name))

def message_handler(update: Update,context: CallbackContext):
    text = update.to_dict()['message']['text']
    update.message.reply_text(text)

if __name__=="__main__":


    bot = Bot(TOKEN)
    bot.set_webhook("https://dd1fd8eaa74f.ngrok.io/" + TOKEN)

    dp = Dispatcher(bot, None)
    dp.add_handler(CommandHandler("start" , greeting))
    dp.add_handler(CommandHandler("help" , help))
    dp.add_handler(MessageHandler(Filters.text , message_handler))
    dp.add_handler(MessageHandler(Filters.sticker ,echo_sticker))
    dp.add_error_handler(error)


    app.run(port=8443)

