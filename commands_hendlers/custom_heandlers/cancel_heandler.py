from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router(name=__name__)


@router.message(Command("cancel❌"))
async def exit_to_menu(message: Message, state: FSMContext) -> None:
    """
    Функция обрабатывает команду /cancel, очищает состояния бота
    и отправляет пользователю информацию о командах бота.\

    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    await state.clear()
    await message.delete()
    await message.answer("Выход в меню команд.")
    await message.answer(
        "/kinodaily - подключение ежедневной рассылки интересных картин любимого жанра.\n\n"
        "Выбиратете жанр кинокартин, время сообщения и бот каждый день будет присылать 1 интересный "
        "фильм"
        "или сериал с описанием в выбраном жанре.\n\n"
        "/topfilms - запрос топ картин в выбранном жанре.\n\n"
        "Бот составляет список лучших или худших по рейтингу картин в выбранных категориях.\n\n"
        "/film - запрос информации о картине по названию.\n\n"
        "Бот выводит информацию о картине, название которой вы напишете в сообщении.\n\n"
        "/history - история ваших запросов боту.\n\n"
        "/help - информация по боту.\n\n"
        "/cancel - выход из любого режима бота в меню команд."
    )
