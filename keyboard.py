from aiogram.types import *


async def start_reply(from_lang, to_lang):
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.add(
        KeyboardButton(from_lang),
        KeyboardButton("🔄"),
        KeyboardButton(to_lang)
    )
    return btn

async def from_lang(languages):
    btn = InlineKeyboardMarkup(row_width=2)
    for i in languages:
        btn.add(
            InlineKeyboardButton(languages[i], callback_data=f"from:{i}")
        )
    return btn
async def to_lang(languages):
    btn = InlineKeyboardMarkup(row_width=2)
    for i in languages:
        if i != "auto":
            btn.add(
                InlineKeyboardButton(languages[i], callback_data=f"to:{i}")
            )
    return btn