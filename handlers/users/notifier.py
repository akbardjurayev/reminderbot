import random
import time
from datetime import datetime
import json
import math

import pytz
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import *

from loader import dp, bot, db
from message.button_text.btn_text import menu_btn_txt
from message.function.get_keyboard_default import get_markup_default
from states.anonim import QuranState
from apscheduler.schedulers.asyncio import AsyncIOScheduler

tz = pytz.timezone('Asia/Tashkent')

job_defaults = {
    "misfire_grace_time": 3600
}

scheduler = AsyncIOScheduler(
    timezone=tz,
    job_defaults=job_defaults
)


async def notifier():
    all_users = await db.select_all_users()
    today = time.strftime("%Y-%m-%d")
    ramazon_day = "2024-03-11"
    date1 = datetime.strptime(today, "%Y-%m-%d")
    date2 = datetime.strptime(ramazon_day, "%Y-%m-%d")
    date_difference = date2 - date1
    number_of_days = date_difference.days
    for user in all_users:
        await bot.send_message(user['telegram_id'], f"Ramazongacha: {number_of_days} kun qoldi!")


hour = random.randrange(24)
minute = random.randrange(60)

# scheduler.add_job(notifier, trigger='interval', seconds=2)
scheduler.add_job(notifier, trigger='cron', hour=hour, minute=minute)
