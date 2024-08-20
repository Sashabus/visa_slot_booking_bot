from telegram import Update
from telegram.ext import ContextTypes

from .keyboard_markups import REPLY_KEYBOARD_START


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome! Please fill out the form to schedule an appointment.",
        reply_markup=REPLY_KEYBOARD_START
    )
