import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from web_project.config_reader import config
from handlers import common
from data import db_session

# to download aiogram 3.x use: pip install -U --pre aiogram

DEFAULT_CITY = "Москва"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


async def main():
    # Запуск БД
    # db_session.global_init("db/place_searcher.db")

    # Настройка диспетчера для правильной работы бота
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.bot_token.get_secret_value())

    # Подключение common-роутера
    dp.include_router(common.router)
    # Ниже подключение роутером для обработки определенных хэндлеров
    # dp.include_router(file_1.router)
    # dp.include_router(file_2.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
