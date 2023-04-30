from datetime import datetime
import logging

from API import yandex_api

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_row import make_row_keyboard

router = Router()

available_cities = ["Москва", "Санкт-Петербург"]
available_transport_types = ["самолет", "поезд", "электричка", "автобус"]


# available_drink_sizes = ["0.2", "0.3", "0.5"]
logging.log(logging.INFO, "init ordering_source.py")

class OrderTicket(StatesGroup):
    choosing_src_place = State()
    choosing_out_place = State()
    choosing_src_date = State()
    choosing_transport_type = State()


@router.message(Command(commands=["order"]))
async def cmd_order(message: Message, state: FSMContext):
    await message.answer(
        text="Приступим к поиску билетов.\n" \
             "Для начала выберите город отправления:",
        reply_markup=make_row_keyboard(available_cities)
    )
    await state.set_state(OrderTicket.choosing_out_place)


@router.message(
    OrderTicket.choosing_out_place,
    F.text.in_(available_cities)
)
async def out_place_chosen(message: Message, state: FSMContext):
    await state.update_data(src_city=message.text)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите город назначения:",
        reply_markup=make_row_keyboard(available_cities)
    )
    await state.set_state(OrderTicket.choosing_src_place)

@router.message(
    OrderTicket.choosing_src_place,
    F.text.in_(available_cities)
)
async def src_place_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    out_city = message.text
    if out_city == user_data["src_city"]:
            await message.answer(
                text="Вы уже указали этот город ранее! Укажите другой город.",
                reply_markup=make_row_keyboard(available_cities)
            )
            await state.set_state(OrderTicket.choosing_src_place)
            return

    await state.update_data(out_city=out_city)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите дату отправления в формате yyyy-mm-dd:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderTicket.choosing_src_date)


@router.message(OrderTicket.choosing_src_place)
async def src_place_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого города.\n\n"
             "Пожалуйста, выберите один из городов ниже:",
        reply_markup=make_row_keyboard(available_cities)
    )

@router.message(OrderTicket.choosing_out_place)
async def src_place_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого города.\n\n"
             "Пожалуйста, выберите один из городов ниже:",
        reply_markup=make_row_keyboard(available_cities)
    )


@router.message(OrderTicket.choosing_src_date)
async def src_date_choosen(message: Message, state: FSMContext):
    date = message.text.lower().replace(":", "-").replace("/", "-")
    await state.update_data(chosen_date=date)
    user_data = await state.get_data()
    try:
        if user_data['chosen_date'] != datetime.strptime(user_data['chosen_date'], "%Y-%m-%d").strftime(
                "%Y-%m-%d"):
            raise ValueError
        await message.answer(
            text=f"Спасибо. Выберите тип транспортного средства:",
            reply_markup=make_row_keyboard(available_transport_types)
        )
        await state.set_state(OrderTicket.choosing_transport_type)

    except ValueError:
        await message.answer(
            text="Вы ввели неправильную дату и время.\n\n"
                 "Пожалуйста, введите дату в правильном формате:",
            reply_markup=ReplyKeyboardRemove())

@router.message(
    OrderTicket.choosing_transport_type,
    F.text.in_(available_transport_types)
)
async def transport_type_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_transport=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f"Спасибо! Ваша поездка сохранена. Вот её данные:\n" \
            f"Из: {user_data['src_city']}\n" \
            f"До: {user_data['out_city']}\n" \
            f"Дата отправления: {user_data['chosen_date']}\n" \
            f"Транспорт: {user_data['chosen_transport']}\n",
        reply_markup=ReplyKeyboardRemove()
    )
    answer = yandex_api.get_schedule(user_data["src_city"], user_data["out_city"], user_data["chosen_date"], user_data["chosen_transport"])
    await message.answer(
        text=answer
    )
    await state.clear()


@router.message(OrderTicket.choosing_src_place)
async def transport_type_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такой тип транспортного средства.\n\n"
             "Пожалуйста, выберите один из городов ниже:",
        reply_markup=make_row_keyboard(available_transport_types)
    )

