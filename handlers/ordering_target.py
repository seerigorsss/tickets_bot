from datetime import datetime
import logging

from API import yandex_api

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_row import make_row_keyboard
from data import db_session
from data.trips import Trips

router = Router()

available_cities = ["Москва", "Санкт-Петербург"]
available_transport_types = ["самолет", "поезд", "электричка", "автобус"]

logging.log(logging.INFO, "init ordering_target.py")


class OrderTargetTicket(StatesGroup):
    choosing_out_date = State()
    choosing_target_transport_type = State()


@router.message(Command(commands=["return"]))
async def cmd_return(message: Message, state: FSMContext):
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, введите дату отправления в формате yyyy-mm-dd:\n" \
             "Для начала выберите город отправления:",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(OrderTargetTicket.choosing_out_date)


@router.message(OrderTargetTicket.choosing_out_date)
async def out_date_chosen(message: Message, state: FSMContext):
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
        await state.set_state(OrderTargetTicket.choosing_target_transport_type)

    except ValueError:
        await message.answer(
            text="Вы ввели неправильную дату и время.\n\n"
                 "Пожалуйста, введите дату в правильном формате:",
            reply_markup=ReplyKeyboardRemove())


@router.message(
    OrderTargetTicket.choosing_target_transport_type,
    F.text.in_(available_transport_types)
)
async def transport_type_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_transport=message.text.lower())
    user_data = await state.get_data()
    db_sess = db_session.create_session()

    # Обращаемся к уже существующей записи о БД в поездке, принадлежащей нашему пользователю
    current_trip = db_sess.query(Trips).filter(Trips.user_id == message.from_user.id).first()
    current_trip.target_date = datetime.strptime(user_data['chosen_date'], '%Y-%m-%d')
    current_trip.target_transport_type = user_data['chosen_transport']
    db_sess.commit()
    await message.answer(
        text=f"Спасибо! Ваша поездка сохранена. Вот её данные:\n\n"
             f'Билет "туда"\n\n' \
             f"Из: {current_trip.source_title}\n" \
             f"До: {current_trip.target_title}\n" \
             f"Дата отправления: {current_trip.source_date}\n" \
             f"Транспорт: {current_trip.source_transport_type}\n\n"
             f'Билет "обратно"\n\n'
             f"Из: {current_trip.target_title}\n" \
             f"До: {current_trip.source_title}\n" \
             f"Дата отправления: {datetime.strptime(user_data['chosen_date'], '%Y-%m-%d')}\n" \
             f"Транспорт: {user_data['chosen_transport']}\n",
        reply_markup=ReplyKeyboardRemove()
    )
    answer, trip = yandex_api.get_schedule(current_trip.target_title, current_trip.source_title,
                                           user_data["chosen_date"],
                                           user_data["chosen_transport"])

    await message.answer(
        text=answer
    )
    await state.clear()


@router.message(OrderTargetTicket.choosing_target_transport_type)
async def transport_type_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такой тип транспортного средства.\n\n"
             "Пожалуйста, выберите один из типов транспорта ниже:",
        reply_markup=make_row_keyboard(available_transport_types)
    )
