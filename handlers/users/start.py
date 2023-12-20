import time
from datetime import datetime
import json
import math

import pytz
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import *

from handlers.users.notifier import notifier
from loader import dp, bot, db
from message.button_text.btn_text import menu_btn_txt
from message.function.get_keyboard_default import get_markup_default
from states.anonim import QuranState


@dp.message_handler(commands='read', state='*')
async def read_pages(mess: Message):
    await mess.answer("Qaysi betgacha qo'qidingiz ?")
    await QuranState.read_page.set()


async def sender(message, day):
    await message.answer('hi')


@dp.message_handler(CommandStart(), chat_type='private', state='*')
async def bot_start(message: Message, state: FSMContext):
    await state.finish()
    today = time.strftime("%Y-%m-%d")
    ramazon_day = "2024-03-11"
    date1 = datetime.strptime(today, "%Y-%m-%d")
    date2 = datetime.strptime(ramazon_day, "%Y-%m-%d")
    date_difference = date2 - date1
    number_of_days = date_difference.days
    await state.update_data(residual_days=number_of_days)
    await message.answer(
        f"Assalomu aleykum {message.from_user.first_name}\nRamazon taxminan 11-martda kiradi!\nBugun: {today}\nRamazongacha: {number_of_days} kun qoldi!\n Quron 604 bet 302 varoq")
    users = await db.select_all_users()
    for user in users:
        if user['telegram_id'] == message.from_user.id:
            break
    else:
        await db.create_user(
            telegram_id=message.from_user.id,
            name=message.from_user.full_name,
            last_page=0,
            page_aim=0
        )
    await message.answer("Siz qaysi betgacha o'qib tugatganingizni yozing:")
    await QuranState.current_page.set()


@dp.message_handler(state=QuranState.current_page)
async def check_username(mess: Message, state: FSMContext):
    residual_pages = 604 - int(mess.text)
    await state.update_data(last_page=int(mess.text))
    state_data = await state.get_data()
    page_each_day = round(residual_pages / state_data['residual_days'])
    goal_last_page = int(mess.text) + page_each_day
    await db.update_user_last_page(int(mess.text), mess.from_user.id)
    await db.update_user_page_aim(page_each_day, mess.from_user.id)
    await mess.answer(
        f"📚 Siz yana {residual_pages} bet quron o'qishingiz kerak!\n\n📖 Siz bir kunda o'rtacha {page_each_day} bet kitob o'qisangiz ramazongacha xatmni tugatasiz in shaa Alloh!\n\n❗️Siz bugun {goal_last_page}-betgacha o'qishingiz kerak!")
    await bot.send_sticker(mess.from_user.id,
                           'CAACAgIAAxkBAAEKy4JlXYT5Dcg4BYvpSm8bEuMDDAhR9AACtREAApo4qEgRHoji-KsbwTME')

    # await db.create_page([])
    # db_dict = {
    #     "last_page": int(mess.text),
    #     "goal_pages": page_each_day,
    #     "goal_last_page": goal_last_page,
    # }

    # file_data = int(mess.text)
    #
    # file = open('db.txt', 'w')
    # file.write(f"{db_dict}")


@dp.message_handler(state=QuranState.read_page)
async def statistic(mess: Message):
    file = open('db.txt', 'r')
    read_file = file.read()
    print(json.loads(read_file))
    # print(file.read())
    # print(type(file.read()))
