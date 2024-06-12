from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime

from app.database.db_requests import save_request, show_history


router = Router(name=__name__)


@router.message(Command("history"))
async def get_history(message: Message) -> None:
    """
    Функция обрабатывает команду /history, делает запрос в базу данных,
    получает информацию о запросах пользователя по его id
    и отправляет ее в чат.

    :param message: Объект сообщения.

    :return:
    None
    """
    await save_request(message.from_user.id, message.text, datetime.now())
    await message.answer(
        f"История запросов:\n {await show_history(message.from_user.id)}"
    )
