import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BotSetings
from Handlers.Neighbor import questionnaire, viewing
from Handlers.Friends import Questionnaire, Viewing
from Handlers.Note import note
from Handlers import Admin, register

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BotSetings.token)
dp = Dispatcher()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(
        register.router,
        questionnaire.router,
        viewing.router,
        Admin.router,
        Questionnaire.router,
        Viewing.router,
        note.router
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
