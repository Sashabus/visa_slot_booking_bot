import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
)

from .keyboard_markups import REPLY_KEYBOARD_FORM, REPLY_KEYBOARD_FORM_END, REPLY_KEYBOARD_START

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define conversation states
NAME, EMAIL, PHONE, REVIEW, REVIEW_DATA = range(5)


# Start the form
async def start_form(update: Update, context: CallbackContext) -> int:
    """Initiate the form by asking for the user's full name."""
    logger.info("Starting form: Asking for user's full name.")
    await update.message.reply_text(
        "Let's start with your full name:",
        reply_markup=REPLY_KEYBOARD_FORM("Firstname Lastname")
    )
    return NAME


# Collect name
async def get_name(update: Update, context: CallbackContext) -> int:
    """Collect the user's full name and proceed to ask for their email."""
    context.user_data['name'] = update.message.text
    logger.info(f"Collected name: {context.user_data['name']}")
    await update.message.reply_text(
        "Great! Now, please enter your email:",
        reply_markup=REPLY_KEYBOARD_FORM("john.doe@example.com")
    )
    return EMAIL


# Collect email
async def get_email(update: Update, context: CallbackContext) -> int:
    """Collect the user's email and proceed to ask for their phone number."""
    context.user_data['email'] = update.message.text
    logger.info(f"Collected email: {context.user_data['email']}")
    await update.message.reply_text(
        "Thanks! Finally, enter your phone number:",
        reply_markup=REPLY_KEYBOARD_FORM()
    )
    return PHONE


# Collect phone number and review inputs
async def get_phone(update: Update, context: CallbackContext) -> int:
    """Collect the user's phone number and present the review of collected data."""
    context.user_data['phone'] = update.message.text
    logger.info(f"Collected phone number: {context.user_data['phone']}")
    return await show_review(update, context)


# Show review with the option to edit or confirm
async def show_review(update: Update, context: CallbackContext) -> int:
    """Show the collected data and provide options to edit or confirm."""
    logger.info("Showing review of collected data.")
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Edit Name", callback_data='edit_name')],
        [InlineKeyboardButton("Edit Email", callback_data='edit_email')],
        [InlineKeyboardButton("Edit Phone", callback_data='edit_phone')],
        [InlineKeyboardButton("Confirm", callback_data='confirm')]
    ])

    await context.bot.send_message(
        update.effective_chat.id,
        f"Here is what you have entered:\n"
        f"Name: {context.user_data['name']}\n"
        f"Email: {context.user_data['email']}\n"
        f"Phone: {context.user_data['phone']}\n\n"
        f"Do you want to make any changes?",
        reply_markup=reply_markup
    )
    return REVIEW


# Handle edits
async def handle_edit(update: Update, context: CallbackContext) -> int:
    """Handle edits to the collected data based on user selection."""
    query = update.callback_query
    await query.answer()

    if query.data == 'edit_name':
        logger.info("User selected to edit the name.")
        await query.edit_message_text("Please enter your full name:")
        context.user_data['current_state'] = NAME
        return REVIEW_DATA
    elif query.data == 'edit_email':
        logger.info("User selected to edit the email.")
        await query.edit_message_text("Please enter your email:")
        context.user_data['current_state'] = EMAIL
        return REVIEW_DATA
    elif query.data == 'edit_phone':
        logger.info("User selected to edit the phone number.")
        await query.edit_message_text("Please enter your phone number:")
        context.user_data['current_state'] = PHONE
        return REVIEW_DATA
    elif query.data == 'confirm':
        logger.info("User confirmed the data.")
        await query.edit_message_text("Thank you! Your data has been confirmed.")
        await context.bot.send_message(
            update.effective_chat.id,
            "Please proceed with the payment:",
            reply_markup=REPLY_KEYBOARD_FORM_END
        )
        return ConversationHandler.END


# Handle new data input after editing
async def handle_new_data(update: Update, context: CallbackContext) -> int:
    """Handle the input for the edited data and return to the review step."""
    current_state = context.user_data.get('current_state')

    if current_state == NAME:
        context.user_data['name'] = update.message.text
        logger.info(f"Updated name: {context.user_data['name']}")
    elif current_state == EMAIL:
        context.user_data['email'] = update.message.text
        logger.info(f"Updated email: {context.user_data['email']}")
    elif current_state == PHONE:
        context.user_data['phone'] = update.message.text
        logger.info(f"Updated phone number: {context.user_data['phone']}")

    # After editing, return to the review step
    return await show_review(update, context)


# Cancel the form
async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancel the form and end the conversation."""
    logger.info("Form canceled by user.")
    await update.message.reply_text("Form canceled.", reply_markup=REPLY_KEYBOARD_START)
    return ConversationHandler.END


# Setup the conversation handler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('form', start_form)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        REVIEW: [
            CallbackQueryHandler(handle_edit)
        ],
        REVIEW_DATA: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_data)
        ]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
