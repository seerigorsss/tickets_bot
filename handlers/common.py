from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

WELCOME_MESSAGE = "Привет! Я - бот по поиску подходящих поездок.\n " \
                  "Могу подобрать вам билет в любой конец мира.\n" \
                  "Доступны: самолет, поезд, электричка, автобус."

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(f'{WELCOME_MESSAGE}\n'
                         f'')


@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
