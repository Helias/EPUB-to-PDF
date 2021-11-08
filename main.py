from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

import os
import subprocess
import logging

# get token from token.conf
TOKEN = open("token.conf", "r").read().strip()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! Send me an epub I will convert it into PDF!")


def conversion(update: Update, context: CallbackContext):
    try:
        if update.message.document:
            file = context.bot.getFile(update.message.document.file_id)
            file_name = update.message.document.file_name

            file_epub = "files/" + file_name
            file_pdf = file_epub.replace(".epub", ".pdf")

            file.download(file_epub)

            update.message.reply_text("Processing... " + file_name)
            subprocess.run(
                ["ebook-convert", file_epub, file_pdf],
                env={"QTWEBENGINE_CHROMIUM_FLAGS": "--no-sandbox"},
            )

            context.bot.send_document(
                chat_id=update.message.chat_id,
                document=open(file_pdf, "rb"),
                caption="Here your PDF!",
            )

            os.remove(file_epub)
            os.remove(file_pdf)
            os.system('find files/ -name "*" ! -iname ".gitkeep" -type f -delete')

        else:
            update.message.reply_text("Send me a file.epub I will convert it into PDF")
    except:
        update.message.reply_text("Error! Please provide valid epub file")


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.document, conversion))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
