from aiogram import executor
import middlewares, filters, handlers
from handlers.users.notifier import scheduler
from loader import dp, db
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Prepare database
    await db.create()
    # # # Create tables
    await db.create_users_table()
    # # Set default commands
    await set_default_commands(dispatcher)

    # Notify admins about bot startup
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
