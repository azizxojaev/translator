import logging
import sqlite3 as sql

from googletrans import Translator, LANGCODES
from aiogram import Bot, Dispatcher, executor, types
from keyboard import *

logging.basicConfig(level=logging.INFO)

translator = Translator()

bot = Bot(token="6366149003:AAHWb_vhPGYyoDRTWbZh9GrXL69h5OiaTos")
dp = Dispatcher(bot)

con = sql.connect("database.db")
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS userData (
    from_lang TEXT,
    to_lang TEXT,
    id INTEGER
)""")

languages = {
    "en": "English 🇺🇸",
    "ru": "Russian 🇷🇺",
    "de": "German 🇩🇪",
    "fr": "French 🇫🇷",
    "it": "Italian 🇮🇹",
    "es": "Spanish 🇪🇸",
    "pl": "Polish 🇵🇱",
    "pt": "Portuguese 🇵🇹",
    "ja": "Japanese 🇯🇵",
    "ko": "Korean 🇰🇷",
    "sv": "Swedish 🇸🇪",
    "da": "Danish 🇩🇰",
    "ar": "Arabic 🇦🇪",
    "auto": "Автоматическое обнаружение 🔎"
}

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    if cur.execute(f"SELECT * FROM userData WHERE id = {message.from_user.id}").fetchone() == None:
        cur.execute("INSERT INTO userData VALUES (?, ?, ?)", ("auto", "en", message.from_user.id))
        con.commit()
    lang1 = cur.execute(f"SELECT from_lang FROM userData WHERE id = {message.from_user.id}").fetchone()[0]
    lang2 = cur.execute(f"SELECT to_lang FROM userData WHERE id = {message.from_user.id}").fetchone()[0]
    btn = await start_reply(languages[lang1], languages[lang2])
    await message.answer("Здравствуйте! Напишите ваш текст а я переведу его на ваш выбранный язык", reply_markup=btn)

@dp.callback_query_handler(text_contains="from:")
async def from_handler(call: types.CallbackQuery):
    lang = call.data.split(':')[1]
    cur.execute(f"UPDATE userData SET from_lang = '{lang}' WHERE id = {call.from_user.id}")
    con.commit()
    lang2 = cur.execute(f"SELECT to_lang FROM userData WHERE id = {call.from_user.id}").fetchone()[0]
    btn = await start_reply(languages[lang], languages[lang2])
    await call.message.answer(f"Вы теперь переводите с {languages[lang]}", reply_markup=btn)
@dp.callback_query_handler(text_contains="to:")
async def to_handler(call: types.CallbackQuery):
    lang = call.data.split(':')[1]
    cur.execute(f"UPDATE userData SET to_lang = '{lang}' WHERE id = {call.from_user.id}")
    con.commit()
    lang2 = cur.execute(f"SELECT from_lang FROM userData WHERE id = {call.from_user.id}").fetchone()[0]
    btn = await start_reply(languages[lang2], languages[lang])
    await call.message.answer(f"Вы теперь переводите на {languages[lang]}", reply_markup=btn)

@dp.message_handler()
async def changeLang_handler(message: types.Message):
    lang1 = cur.execute(f"SELECT from_lang FROM userData WHERE id = {message.from_user.id}").fetchone()[0]
    lang2 = cur.execute(f"SELECT to_lang FROM userData WHERE id = {message.from_user.id}").fetchone()[0]
    if message.text in languages[lang1]:
        btn = await from_lang(languages)
        await message.answer("С какого языка хотите перевести?", reply_markup=btn)
    elif message.text in languages[lang2]:
        btn = await to_lang(languages)
        await message.answer("На какой язык хотите перевести?", reply_markup=btn)
    elif message.text == "🔄":
        if lang1 != "auto":
            cur.execute(f"UPDATE userData SET from_lang = '{lang2}' WHERE id = {message.from_user.id}")
            cur.execute(f"UPDATE userData SET to_lang = '{lang1}' WHERE id = {message.from_user.id}")
            con.commit()
            btn = await start_reply(languages[lang2], languages[lang1])
            await message.answer(f"Вы теперь переводите с {languages[lang2]} на {languages[lang1]}", reply_markup=btn)
        else:
            await message.answer("Нельзя поменять местами если вы переводите с автоматического обнаружения!")
    else:
        result = translator.translate(text=message.text, src=lang1, dest=lang2)
        await message.answer(result.text.capitalize())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
