from datetime import datetime
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.database.db_requests import save_request, get_film_info
from app.utils import open_url, send_film_info, cancel_massege


router = Router(name=__name__)


class Film(StatesGroup):
    name = State()


@router.message(Command("film"))
async def film_info(message: Message, state: FSMContext) -> None:
    """
    Функция обрабатывает команду /film,
    устанавливает состояние и запрашивает название фильма.

    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    await save_request(message.from_user.id, message.text, datetime.now())
    await state.set_state(Film.name)
    await message.answer("Название фильма или сериала:")


@router.message(Film.name)
async def film_name(message: Message, state: FSMContext) -> None:
    """
    Функция обрабатывает ввод названия, формирует API-запрос,
    получает информацию о фильме, отпраляет пользователю
    и очищает состояния бота.

    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    if not message.text.startswith("/cancel"):
        delete_mess = await message.answer(
            "Подождите секунду...", disable_notification=True
        )
        try:
            await state.update_data(name=message.text)
            await message.bot.send_chat_action(
                chat_id=message.chat.id, action=ChatAction.TYPING
            )

            data = await state.get_data()
            film_name = data.get("name")
            res_file = await get_film_info(film_name)

            await send_film_info(message, res_file)
            await message.bot.delete_message(
                chat_id=message.chat.id, message_id=delete_mess.message_id
            )
        except:
            await message.answer(
                "Такого у меня в базе не нашлось...\n\n"
                "Попробуйте еще раз. \nВведите команду /film"
            )
            await message.bot.delete_message(
                chat_id=message.chat.id, message_id=delete_mess.message_id
            )
    else:
        await message.answer(cancel_massege())
    await state.clear()
