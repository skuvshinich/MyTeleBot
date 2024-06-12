from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from datetime import datetime

from app.database.db_requests import save_request, get_film, create_notice
from app.utils import send_film_info, cancel_massege
from app import keyboards as kb

import asyncio
import re

router = Router()


class Notice(StatesGroup):
    genre = State()
    time = State()


@router.message(Command("kinodaily"))
async def kinodaily1(message: Message, state: FSMContext) -> None:
    """
    Функция обрабатывает команду /kinodaily,
    устанавливает состояние и запрашивает у пользователя жанр.

    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    await save_request(message.from_user.id, message.text, datetime.now())
    await state.set_state(Notice.genre)
    await message.answer(
        "Выберите ваш любимый жанр фильмов:", reply_markup=kb.keyboard6
    )


@router.message((lambda message: message.text not in kb.genres[1:]), Notice.genre)
async def check_genre(message: Message, state: FSMContext) -> None:
    """
    Функция проверки ввода при выборе жанра

    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    if not message.text.startswith("/cancel"):
        await state.set_state(Notice.genre)
        await message.answer(
            "Такой жанр вы выбрать не можете.\n" "Выберите жанр на клавиатуре.",
            reply_markup=kb.keyboard6,
        )
    else:
        await message.answer(cancel_massege())
        await state.clear()


@router.message(Notice.genre)
async def kinodaily2(message: Message, state: FSMContext) -> None:
    """
    Функция обрабатывает ввод при выборе жанра,
    устанавливает состояние и запрашивает время получения сообщения.

    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    await state.update_data(genre=message.text)
    await state.set_state(Notice.time)
    await message.answer(
        "В какое время вам будет получать сообщение от бота?\n"
        "Напишите время в формате (ЧЧ:ММ):"
    )


@router.message(
    lambda message: not re.match(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$", message.text),
    Notice.time,
)
async def check_time(message: Message, state: FSMContext) -> None:
    """
    Функция проверки ввода при выборе времени получения сообщения от бота.

    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    if not message.text.startswith("/cancel"):
        await state.set_state(Notice.time)
        await message.answer(
            "Кажется неверный формат времени...\n"
            "Попробуйте еще раз.\n"
            "Напишите время в формате (ЧЧ:ММ):"
        )
    else:
        await message.answer(cancel_massege())
        await state.clear()


@router.message(Notice.time)
async def kinodaily3(message: Message, state: FSMContext) -> None:
    """
    Функция обрабатывает ввод при выборе времени получения сообщения, очищает состояния бота,
    переходит в бесконечный цикл, ежеминутно проверяющий соответствие времени
    и отрпавляет в назначенное пользователем время информацию о фильме.


    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    if not message.text.startswith("/cancel"):
        await state.update_data(time=message.text)
        data = await state.get_data()
        await create_notice(message.from_user.id, data["genre"], data["time"])
        await message.answer(
            f"Отлично! Сообщение будет отправляться каждый день!"
            f'\n Жанр фильмов: {data["genre"]}'
            f'\n Время получения сообщения {data["time"]}'
        )
        await state.clear()

        while True:
            current_time = datetime.now().strftime("%H:%M")
            if current_time == data["time"]:
                film = await get_film(message.from_user.id, data["genre"])
                await send_film_info(message, film)

            await asyncio.sleep(60)  # Проверка каждую минуту
    else:
        await message.answer(cancel_massege())
        await state.clear()


# def check_time_format(time):
#     if re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', time):
#         return True
#     return False
