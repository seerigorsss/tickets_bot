import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
import dotenv
import os
from user import UserHandler
from place import PlaceHandler
import messages as msg
from weather import Weather, WeatherHandler


DEFAULT_CITY = "Москва"

user_handler = UserHandler()
place_handler = PlaceHandler()
weather_handler = WeatherHandler()

place_handler.load_places()
user_handler.load_users()

dotenv.load_dotenv(dotenv.find_dotenv())
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Получить аккаунт или создать новый
def user_check(message: types.Message):
    from_id = message.from_id
    if user_handler.is_user(from_id):
        return user_handler.get_user(from_id)
    user = user_handler.create_user(from_id)
    return user

# Начальное сообщение
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    user = user_check(message)
    await message.answer(msg.WELCOME_MESSAGE)

# Установить город
@dp.message_handler(commands=["set_city"])
async def cmd_start(message: types.Message):
    user = user_check(message)
    user.set_city("Стерлитамак") # TODO: Сделать смену городов
    await message.answer(msg.WELCOME_MESSAGE)

# Получить случайное место или мероприятие в городе
@dp.message_handler(commands=["get_place"])
async def cmd_start(message: types.Message):
    user = user_check(message)
    city = None
    if user.has_city():
        city = user.get_city()
        temperature, weather = weather_handler.get_weather(city)
    else:
        temperature, weather = weather_handler.get_weather(DEFAULT_CITY)

    place_list = []
    if city is not None:
        place_list = place_handler.get_places_limited_by_city(city, temperature, weather)
    else:
        place_list = place_handler.get_places(temperature, weather)

    # TODO: вывести случайное место и добавить кнопку "Посетил", чтобы за него начислили очки
    await message.answer(msg.WELCOME_MESSAGE)

# Профиль
@dp.message_handler(commands=["profile"])
async def cmd_start(message: types.Message):
    user = user_check(message)
    answer_msg = msg.PROFILE_MESSAGE.replace("%score%", str(user.score)) \
                                    .replace("%places_len%", str(user.get_len_places())) \
                                    .replace("%place_city%", user.get_city())
    await message.answer(answer_msg)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
