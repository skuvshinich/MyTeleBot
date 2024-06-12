from aiogram import Router
from aiogram.types import Message

router = Router(name=__name__)


@router.message()
async def echo(message: Message) -> None:
    """
    Функция обрабатывает сообщения пользователя, которые не обрабоались всеми остальными обработчиками бота.

    :param message: Объект сообщения.

    :return:
    None
    """
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply("Что-то новое...☺")
