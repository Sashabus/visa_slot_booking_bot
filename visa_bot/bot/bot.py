from telegram.ext import ApplicationBuilder, CommandHandler

from handlers.start import start
from handlers.form import conv_handler

import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")


def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
