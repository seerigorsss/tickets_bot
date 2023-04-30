from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_row import make_row_keyboard

router = Router()

available_drink_names = ["Чай", "Кофе", "Газировка"]
available_drink_sizes = ["0.2", "0.3", "0.5"]


class OrderDrink(StatesGroup):
    choosing_drink_name = State()
    choosing_drink_size = State()


@router.message(Command("drinks"))
async def cmd_drink(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите напиток:",
        reply_markup=make_row_keyboard(available_drink_names)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(OrderDrink.choosing_drink_name)


@router.message(
    OrderDrink.choosing_drink_name,
    F.text.in_(available_drink_names)
)
async def drink_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_drink=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите объем напитка:",
        reply_markup=make_row_keyboard(available_drink_sizes)
    )
    await state.set_state(OrderDrink.choosing_drink_size)


@router.message(OrderDrink.choosing_drink_name)
async def drink_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого напитка.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(available_drink_names)
    )


@router.message(OrderDrink.choosing_drink_size, F.text.in_(available_drink_sizes))
async def drink_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали  {user_data['chosen_drink']} с объемом {message.text.lower()} литра.\n"
             f"Попробуйте теперь заказать блюда: /food",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(OrderDrink.choosing_drink_size)
async def drink_size_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого объема напитка.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(available_drink_sizes))
