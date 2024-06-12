from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.enums import ChatAction
from datetime import datetime

from app.database.db_requests import save_request
from app import keyboards as kb
from app.utils import create_top_films, cancel_massege

router = Router(name = __name__)


class Top(StatesGroup):
    rvrs = State()
    top = State()
    movie_type = State()
    genre = State()
    kinosite = State()
    limit = 250


@router.message(Command("topfilms"))
async def top_films1(message: Message, state: FSMContext) -> None:
    """
    Функция обрабатывает команду /topfilms для подборки топа фильмов,
    устанавливает состояние и запрашивает формат топа.


    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    await save_request(message.from_user.id, message.text, datetime.now())
    await state.set_state(Top.rvrs)
    await message.answer("Какой топ хотите подобрать?", reply_markup = kb.keyboard1)


@router.message(lambda message: message.text not in ["лучшие", "худшие"], Top.rvrs)
async def check_format(message: Message, state: FSMContext) -> None:
    """
    Функция проверки ввода при выборе формата топа.

    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    if not message.text.startswith("/cancel"):
        await state.set_state(Top.rvrs)
        await message.answer(
            "Что-то не то... Давайте еще раз.\n" "Какой топ хотите подобрать?",
            reply_markup = kb.keyboard1,
        )
    else:
        await message.answer(cancel_massege())
        await state.clear()


@router.message(Top.rvrs)
async def top_films2(message: Message, state: FSMContext) -> None:
    """
    Функция обрабатывает ввод при выборе формата топа,
    устанавливает состояние и запрашивает количество позиций в топе.


    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    if message.text == "лучшие":
        await state.update_data(rvrs = True)
    elif message.text == "худшие":
        await state.update_data(rvrs = False)
    await state.set_state(Top.top)
    await message.answer(
        "Укажите количество позиций в топе:", reply_markup = kb.keyboard2
    )


@router.message(lambda message: message.text not in ["5", "10", "25", "100"], Top.top)
async def quantity_check(message: Message, state: FSMContext) -> None:
    """
    Функция проверки ввода при выборе количества позиций в топе.

    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    if not message.text.startswith("/cancel"):
        await state.set_state(Top.top)
        await message.answer(
            "Выберите количество позиций в топе:", reply_markup = kb.keyboard2
        )
    else:
        await message.answer(cancel_massege())
        await state.clear()


@router.message(Top.top)
async def top_films3(message: Message, state: FSMContext) -> None:
    """
    Функция обрабатывает ввод при выборе количества позиций в топе,
    устанавливает состояние и запрашивает видеоформат.


    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    await state.update_data(top = int(message.text))
    await state.set_state(Top.movie_type)
    await message.answer("Выберете видеоформат:", reply_markup = kb.keyboard3)


@router.message(
    lambda message: message.text
                    not in ["аниме", "мультфильмы", "фильмы", "сериалы", "мультсериалы"],
    Top.movie_type,
)
async def type_check(message: Message, state: FSMContext) -> None:
    """
    Функция проверки ввода при выборе видеоформата.

    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    if not message.text.startswith("/cancel"):
        await state.set_state(Top.movie_type)
        await message.answer(
            "Всё же... Выберете видеоформат на клавиатуре:", reply_markup = kb.keyboard3
        )
    else:
        await message.answer(cancel_massege())
        await state.clear()


@router.message(Top.movie_type)
async def top_films4(message: Message, state: FSMContext) -> None:
    """
    Функция обрабатывает ввод при выборе видеоформата,
    устанавливает состояние и запрашивает жанр фильмов.


    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    if message.text == "фильмы":
        await state.update_data(movie_type = "movie")
    elif message.text == "сериалы":
        await state.update_data(movie_type = "tv-series")
    elif message.text == "мультфильмы":
        await state.update_data(movie_type = "cartoon")
    elif message.text == "мультсериалы":
        await state.update_data(movie_type = "animated-series")
    elif message.text == "аниме":
        await state.update_data(movie_type = "anime")
    await state.set_state(Top.genre)
    await message.answer("Выберите жанр:", reply_markup = kb.keyboard4)


@router.message((lambda message: message.text not in kb.genres), Top.genre)
async def genre_check(message: Message, state: FSMContext) -> None:
    """
    Функция проверки ввода при выборе жанра.

    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    if not message.text.startswith("/cancel"):
        await state.set_state(Top.genre)
        await message.answer(
            "Такой жанр вы выбрать не можете.\n" "Выберите жанр на клавиатуре:",
            reply_markup = kb.keyboard6,
        )
    else:
        await message.answer(cancel_massege())
        await state.clear()


@router.message(Top.genre)
async def top_films6(message: Message, state: FSMContext) -> None:
    """
    Функция обрабатывает ввод при выборе жанра,
    устанавливает состояние и запрашивает выбор киносайта.


    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    if message.text == "все жанры":
        await state.update_data(genre = None)
    else:
        await state.update_data(genre = message.text)
    await state.set_state(Top.kinosite)
    await message.answer(
        "Рейтинг какого сервиса будем учитывать?", reply_markup = kb.keyboard5
    )


@router.message(lambda message: message.text not in ["Kinopoisk", "IMDb"], Top.kinosite)
async def check_site(message: Message, state: FSMContext) -> None:
    """
    Функция проверки ввода при выборе киносайта.

    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    if not message.text.startswith("/cancel"):
        await state.set_state(Top.kinosite)
        await message.answer(
            "Выберите сервис на клавиатуре:", reply_markup = kb.keyboard5
        )
    else:
        await message.answer(cancel_massege())
        await state.clear()


@router.message(Top.kinosite)
async def top_films6(message: Message, state: FSMContext) -> None:
    """
    Функция обрабатывает ввод при выборе киносайта,
    формирует API-запрос из полученных данных,
    получает топ-фильмов по заданным пользователем параметрам,
    отправляет в чат и очищает состояния бота.


    :param message: Объект сообщения.
    :param state: Объект FSM контекста.

    :return:
    None
    """
    site_name = message.text
    if message.text == "Kinopoisk":
        await state.update_data(kinosite = "kp")
    elif message.text == "IMDb":
        await state.update_data(kinosite = "imdb")

    context_data = await state.get_data()
    limit = Top.limit
    genre = context_data.get("genre")
    movie_type = context_data.get("movie_type")
    rvrs = context_data.get("rvrs")
    kinosite = context_data.get("kinosite")
    top = context_data.get("top")
    page = 1  # if rvrs == True else 2
    url = (
        f"https://api.kinopoisk.dev/v1.4/movie?page={page}&limit={limit}&type={movie_type}"
        if genre is None
        else f"https://api.kinopoisk.dev/v1.4/movie?page={page}&limit={limit}&type={movie_type}&genres.name={genre}"
    )
    delete_mess = await message.answer(
        "Подождите секунду...", disable_notification = True
    )
    await message.bot.send_chat_action(
        chat_id = message.chat.id, action = ChatAction.TYPING
    )
    try:
        query_result = create_top_films(url, rvrs, kinosite, top)
        best_photo = (
            "https://www.annarusska.ru/upload/resize_cache/content/525"
            "/1100_739_1619711fa078991f0a23d032687646b21/52589637826953f71b49868feb3eb2c3.jpg"
        )
        worst_photo = "https://wp.dailybruin.com/images/2014/02/0bf92348-ee7c-406d-9e9d-1105b3adace1.jpg"
        pic = best_photo if rvrs == True else worst_photo
        await message.bot.send_photo(
            chat_id = message.chat.id,
            photo = pic,
            caption = f"<u>Топ по версии {site_name}</u>:\n\n{query_result}",
            parse_mode = "HTML",
        )

    except Exception:
        await message.answer(
            "УПС... Кажется что-то не так.\n"
            "Попробуйте еще раз или сделайте запрос позже."
        )
    await message.bot.delete_message(
        chat_id = message.chat.id, message_id = delete_mess.message_id
    )

    await state.clear()
