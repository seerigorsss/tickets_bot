from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from data import db_session
from data.users import User
from data.trips import Trips

WELCOME_MESSAGE = "Привет! Я - бот по поиску подходящих поездок.\n" \
                  "Могу подобрать вам билет в любой конец мира.\n" \
                  "Доступны: самолет, поезд, электричка, автобус.\n"
ORDER_MESSAGE = "Чтобы найти билет, напишите /order."
CANCEL_MESSAGE = "Чтобы отменить заказ билетов, напишите /cancel."
NO_TRIPS_MESSAGE = "У вас нет запланированных поездок."
TRIP_INFO_MESSAGE = "Поездка из %city1% в %city2% на %transport%; Дата: %date%"

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    user_info = message.from_user
    db_sess = db_session.create_session()
    # Если пользователя нет в БД, то заносим его
    if not db_sess.query(User).filter(User.telegram_id == user_info.id).first():
        user = User(
            telegram_id=user_info.id,
            first_name=user_info.first_name,
            second_name=user_info.last_name
        )
        db_sess.add(user)
        db_sess.commit()
    await message.answer("\n".join([WELCOME_MESSAGE, ORDER_MESSAGE, CANCEL_MESSAGE]))


@router.message(Command('get_trips'))
async def cmd_start(message: types.Message):
    user_info = message.from_user
    db_sess = db_session.create_session()
    # Если пользователя нет в БД, то заносим его
    if not db_sess.query(User).filter(User.telegram_id == user_info.id).first():
        user = User(
            telegram_id=user_info.id,
            first_name=user_info.first_name,
            second_name=user_info.last_name
        )
        db_sess.add(user)
        db_sess.commit()
        await message.answer(NO_TRIPS_MESSAGE)
        return
    user = db_sess.query(User).filter(User.telegram_id == user_info.id).first()
    trips = db_sess.query(Trips).filter(Trips.user_id == user.id).order_by(Trips.source_date).all()
    if len(trips) == 0:
        await message.answer(NO_TRIPS_MESSAGE)
        return
    answer_message = ["Ваши поездки:"]
    for trip in trips:
        answer_message.append(TRIP_INFO_MESSAGE.replace("%city1%", trip.source_title) \
                              .replace("%city2", trip.target_title) \
                              .replace("%transport%", trip.source_transport_type) \
                              .replace("%date%", trip.source_date))
    await message.answer("\n".join(answer_message))

@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=f"Действие отменено\n"
             f"{ORDER_MESSAGE}",
        reply_markup=ReplyKeyboardRemove()
    )
