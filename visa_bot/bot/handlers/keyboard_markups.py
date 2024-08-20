from telegram import (
    ReplyKeyboardMarkup
)

REPLY_KEYBOARD_START = ReplyKeyboardMarkup(
    [['/form']],
    one_time_keyboard=True
)


def REPLY_KEYBOARD_FORM(input_field_placeholder=None):
    reply_keyboard = ReplyKeyboardMarkup(
        [['/cancel']],
        one_time_keyboard=True,
        input_field_placeholder=input_field_placeholder
    )
    return reply_keyboard


REPLY_KEYBOARD_FORM_END = ReplyKeyboardMarkup(
    [['Pay Now', '/Cancel']],
    one_time_keyboard=True
)
