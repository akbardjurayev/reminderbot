from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_markup_default(language, btn_txt):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    text = btn_txt[language]
    for btn_text in text:
        button = KeyboardButton(text=btn_text)
        markup.insert(button)
    return markup


async def get_markup_default_phone(language, btn_txt):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    text = btn_txt[language]
    for btn_text in text:
        button = KeyboardButton(text=btn_text, request_contact=True)
        markup.insert(button)
    return markup
