from aiogram import types, Router, F
from aiogram.filters import CommandStart, or_f, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_quiz, orm_add_user
from filters.chat_types import ChatTypeFilter

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


class AddQuiz(StatesGroup):
    wedding_date = State()
    wedding_location = State()
    cuisine = State()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    await message.answer('Начало работы.')


##### FSM #####
# Встаем в ожидание ввода даты
@user_private_router.message(StateFilter(None), or_f(Command('quiz'), F.text.casefold() == 'опросник'))
async def quiz(message: types.Message, state: FSMContext, session: AsyncSession):
    user = message.from_user
    await orm_add_user(
        session,
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=None,
    )
    await message.answer('Введите дату свадьбы в формате: YYYY-MM-DD')
    await state.set_state(AddQuiz.wedding_date)


# Ловим дату, встаем в ожидание локации
@user_private_router.message(AddQuiz.wedding_date, F.text)
async def add_wedding_date(message: types.Message, state: FSMContext):
    await state.update_data(wedding_date=date.fromisoformat(message.text))
    await message.answer('Введите локацию свадьбы')
    await state.set_state(AddQuiz.wedding_location)


# Ловим локацию, встаем в ожидание выбора кухни
@user_private_router.message(AddQuiz.wedding_location, F.text)
async def add_wedding_location(message: types.Message, state: FSMContext):
    await state.update_data(wedding_location=message.text)
    await message.answer('Введите предпочитаемую кухню')
    await state.set_state(AddQuiz.cuisine)


# Ловим кухню, записываем все в базу, и выходим из FSM
@user_private_router.message(AddQuiz.cuisine, F.text)
async def add_cuisine(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(cuisine=message.text)

    data = await state.get_data()
    data['user_id'] = message.from_user.id
    await orm_add_quiz(session, data)

    await message.answer('Данные собраны и добавлены в базу')
    await state.clear()
