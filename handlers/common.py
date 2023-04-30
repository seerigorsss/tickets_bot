from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
import time

WELCOME_MESSAGE = "Привет! Я - бот по поиску подходящих поездок.\n" \
                  "Могу подобрать вам билет в любой конец мира.\n" \
                  "Доступны: самолет, поезд, электричка, автобус.\n"
ORDER_MESSAGE = "Чтобы найти билет, напишите /order."
CANCEL_MESSAGE = "Чтобы отменить заказ билетов, напишите /cancel."

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(WELCOME_MESSAGE)
    await message.answer(ORDER_MESSAGE)
    await message.answer(CANCEL_MESSAGE)


@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=f"Действие отменено\n"
             f"{ORDER_MESSAGE}",
        reply_markup=ReplyKeyboardRemove()
    )


