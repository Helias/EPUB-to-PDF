from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, CallbackQueryHandler, Filters, CallbackContext

import logging
import os
import sys

# get token from token.conf
TOKEN = open("token.conf", "r").read().strip()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
  update.message.reply_text('Hi! Send me an epub I will convert it into PDF!')

def conversion(update: Update, context: CallbackContext):

    if update.message.document:
        file_name=update.message.document.file_name
        full_path = "files/" + file_name
        file = context.bot.getFile(update.message.document.file_id)
        file.download(full_path)
        update.message.reply_text('Processing...' + file_name)
        file_pdf = full_path.replace(".epub", ".pdf")

        print("####################################")
        print('ebook-convert "' + full_path + '" "' + file_pdf + '"')
        print("####################################")

        os.system('ebook-convert "' + full_path + '" "' + file_pdf + '"') # conversion to PDF
        context.bot.send_document(chat_id=update.message.chat_id, document=open(file_pdf, 'rb'), caption="Here your PDF!")
        os.remove(full_path)
        os.remove(file_pdf)
        os.system('find files/ -name "*" ! -iname ".gitkeep" -type f -delete')
    else:
        update.message.reply_text('Send me a file.epub I will convert it into PDF')

def main():
  updater = Updater(TOKEN, use_context=True)

  dp = updater.dispatcher

  dp.add_handler(MessageHandler(Filters.document, conversion))
  dp.add_handler(CommandHandler('start', start))
  dp.add_handler(CommandHandler('help', start))

  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
    main()
