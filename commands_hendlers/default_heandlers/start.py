from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database import db_requests as rq

router = Router(name=__name__)


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    """
    Функция обрабатывает команду /start и пишет в чат приветствие.

    :param message: Объекст сообщения.

    :return:
    None
    """
    await rq.set_user(message.from_user.id, message.from_user.username)
    await message.bot.send_photo(
        chat_id=message.chat.id,
        photo="https://img.freepik.com/free-photo/cinematography-stuff-black-background_23-2147698944.jpg?t=st=1716215814~exp=1716219414~hmac=14b729a932184def4c5c94661f6e2e7e2c4e3192394b90c7ffbc720d7726e64e&w=1060",
        caption=f"<b>Привет, {message.from_user.first_name}</b>!\n"
        f"Я - Телеграм Бот удобной подборки фильмов и сериалов для просмотра.\n"
        f"Чтобы понять, что я умею нажмите команду ➡ /help",
        parse_mode="HTML",
    )
    await message.delete()
