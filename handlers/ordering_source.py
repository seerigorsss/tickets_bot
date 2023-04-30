from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_row import make_row_keyboard
from filters.correct_date_time import DateTimeFilter

router = Router()

available_cities = ["Москва", "Санкт-Петербург"]


# available_drink_sizes = ["0.2", "0.3", "0.5"]


class OrderTicket(StatesGroup):
    choosing_src_place = State()
    choosing_src_date = State()
    choosing_trg_place = State()
    choosing_trg_date = State()


@router.message(Command("order"))
async def cmd_order(message: Message, state: FSMContext):
    await message.answer(
        text="Приступим к поиску билетов.\n"
             "Для начала выберите город отправки:",
        reply_markup=make_row_keyboard(available_cities)
    )
    # Устанавливаем пользователю состояние "выбирает город отправки"
    await state.set_state(OrderTicket.choosing_src_place)


@router.message(
    OrderTicket.choosing_src_place,
    F.text.in_(available_cities)
)
async def place_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_city=message.text)
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите дату и время в формате hh-mm dd-mm-yy:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(OrderTicket.choosing_src_date)


@router.message(OrderTicket.choosing_src_place)
async def place_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого города.\n\n"
             "Пожалуйста, выберите один из городов ниже:",
        reply_markup=make_row_keyboard(available_cities)
    )


@router.message(OrderTicket.choosing_src_date)
async def drink_size_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_date=message.text.lower())
    user_data = await state.get_data()
    try:
        if user_data['chosen_date'] != datetime.strptime(user_data['chosen_date'], "%H-%M %d-%m-%Y").strftime(
                "%H-%M %d-%m-%Y"):
            raise ValueError
        await message.answer(
            text=f"Вы выбрали  город {user_data['chosen_city']} и дату {user_data['chosen_date']}.\n",
        )
        await state.set_state(OrderTicket.choosing_trg_date)

    except ValueError:
        await message.answer(
            text="Вы ввели неправильную дату и время.\n\n"
                 "Пожалуйста, введите дату в правильном формате:",
            reply_markup=ReplyKeyboardRemove())

# @router.message(OrderTicket.choosing_src_date)
# async def drink_size_chosen_incorrectly(message: Message):
#     await message.answer(
#         text="Вы ввели неправильную дату и время.\n\n"
#              "Пожалуйста, введите дату в правильном формате:",
#         reply_markup=ReplyKeyboardRemove())
