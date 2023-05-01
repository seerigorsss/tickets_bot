import asyncio
import logging
from API import yandex_api
from data import db_session

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_reader import config
from handlers import common, ordering_source, ordering_target

# to download aiogram 3.x use: pip install -U --pre aiogram

DEFAULT_CITY = "Москва"


async def main():
    # Запуск БД
    db_session.global_init("db/place_searcher.db")

    yandex_api.load_data()

    # Настройка диспетчера для правильной работы бота
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    # Подключение роутеров
    dp.include_router(common.router)
    dp.include_router(ordering_source.router)
    dp.include_router(ordering_target.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
