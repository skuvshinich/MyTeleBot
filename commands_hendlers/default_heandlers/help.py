from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name=__name__)


@router.message(Command("help"))
async def help(message: Message) -> None:
    """
    Функция обрабатывает команду /help и выводит пользователю информацию о командах бота.

    :param message: Объект сообщения.

    :return:
    None
    """
    await message.bot.send_photo(
        chat_id=message.chat.id,
        photo="https://img.freepik.com/free-photo/film-projector-with-popcorn-box_23-2148115326.jpg?t=st=1716215254~exp=1716218854~hmac=8fe8685ac478c0416498565e290dd56771525d48d1baabcd1a6f0edd825e63b3&w=1060",
        caption="ИНФОРМАЦИЯ ПО БОТУ\n"
        "Что умеет бот?\n\n"
        "/kinodaily - подключение ежедневной рассылки интересных картин любимого жанра.\n"
        "Выбиратете жанр кинокартин, время сообщения и бот каждый день будет присылать 1 интересный фильм"
        " или сериал с описанием в выбраном жанре.\n\n"
        "/topfilms - запрос топa картин в выбранном жанре.\n\n"
        "Бот составляет список лучших или худших по рейтингу картин в выбранных категориях.\n\n"
        "/film - запрос информации о картине по названию.\n"
        "Бот выводит информацию о картине, название которой вы напишете в сообщении.\n\n"
        "/history - история ваших запросов боту.\n\n"
        "/help - информация по боту.\n\n"
        "/cancel - выход из любого режима бота в меню команд.",
    )
