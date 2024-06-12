import requests
import json
from typing import Any

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from googletrans import Translator

from config_data.config import API_KEY


def open_url(url: str) -> Any:
    """
    Функция для открытия URL-адреса и получения данных.

    :param url: cтрока с URL-адресом, который требуется открыть.

    :return:
    Возвращает данные, полученные из URL-адреса в формате JSON.
    """
    headers = {"accept": "application/json", "X-API-KEY": API_KEY}

    response = requests.get(url, headers=headers)
    file = json.loads(response.text)

    return file


def print_top(film_list: list, rvrs: bool) -> str:
    """
    Функция форматирует топ-фильмов для выводы в чат пользователю.

    :param film_list: Список фильмов для вывода.
    :param rvrs: Флаг для указания направления сортировки.

    :return:
    Возвращае строку с отформатированнным топом.
    """
    res_str = str()
    first = "🏆" if rvrs == True else "🤬"
    second = "🥈" if rvrs == True else "🤡"
    third = "🥉" if rvrs == True else "👎"
    for film in film_list:
        index = film_list.index(film)
        if index == 0:
            res_str += f"<b>{index + 1}. {film[0]}</b> - {film[1]} {first}\n"
        elif index == 1:
            res_str += f"<b>{index + 1}. {film[0]}</b> - {film[1]} {second}\n"
        elif index == 2:
            res_str += f"<b>{index + 1}. {film[0]}</b> - {film[1]} {third}\n"
        else:
            res_str += f"{index + 1}. {film[0]} - {film[1]}\n"

    return res_str


def create_top_films(url: str, rvrs: bool, kinosite: str, top: int) -> str:
    """
    Функция формирует топ-фильмов на основе переданных параметров.

    :param url: URl для получения данных о фильмах.
    :param rvrs: Флаг для указания направления сортировки
    :param kinosite: Строка с информацией о выбранном сервисе для определения рейтинга.
    :param top: Количество позиций в создаваемом топе.

    :return:
    Возвращает отформатированныую строку топа.
    """

    try:
        file = open_url(url)

        # with open('test3.json', 'w', encoding = 'utf8') as tst:
        #      json.dump(file, tst, ensure_ascii = False, indent = 4)

        films = file["docs"]

        top_films = sorted(
            {
                film["name"]: film["rating"][kinosite]
                for film in films
                if film["rating"][kinosite] != 0 and film["name"] != None
            }.items(),
            key=lambda film: film[1],
            reverse=rvrs,
        )

        return print_top(top_films[:top], rvrs)
    except Exception:
        return "Error"


async def send_film_info(message: Message, film: dict) -> None:
    """
    Функция форматирует информацию о фильме из словаря, превращая ее в строку, и отрпавляет пользователю.

    :param message: Сообщение пользователя.
    :param film: Словарь, содержащий информацию о фильме.

    :return:
    None
    """
    info = list()
    info.append(film["poster"]["url"])
    en_type = film["type"]
    translator = Translator()
    ru_type = translator.translate(en_type, src="en", dest="ru").text
    info.append(f"🎥 <b>{ru_type.title()}</b>: {film['name']} ({film['year']})")
    info.append(f"      <i>{film['countries'][0]['name']}</i>\n")
    info.append(f"🔶 <i>{film['description']}</i>\n")  # <b>Сюжет</b>
    info.append(
        f"<b>Жанр</b>: {', '.join([item for items in [i.values() for i in film['genres']] for item in items])}.\n"
    )
    info.append(
        f'<b>Главные роли</b>: {", ".join([person["name"] for person in film["persons"][:3] if person is not None])}.\n'
    )
    info.append(
        f"📊 <b>Kinopoisk</b>: {film['rating']['kp']} | <b>IMDB</b>: {film['rating']['imdb']}"
    )

    try:
        markup = None
        if "videos" in film:
            trailer = InlineKeyboardButton(
                text="трейлер", url=film["videos"]["trailers"][0]["url"]
            )  # <a href="ссылка">текст</a>
            row = [trailer]
            rows = [row]
            markup = InlineKeyboardMarkup(inline_keyboard=rows)

        query_result = "\n".join(info[1:])
        url_poster = info[0]
        await message.bot.send_photo(
            chat_id=message.chat.id,
            photo=url_poster,
            caption=query_result,
            reply_markup=markup,
            parse_mode="HTML",
        )
    except Exception:
        await message.answer(
            "УПС... Кажется что-то не так...\n"
            "Не получилось выполнить ваш запрос(((..."
        )


def cancel_massege() -> str:
    """
    Функция возвращает информацию о командах бота.

    :return:
    Строка с информацией о командах бота.
    """
    return (
        "/notice - подключение ежедневной рассылки интересных картин любимого жанра.\n"
        "\nВыбиратете жанр кинокартин, время сообщения и бот каждый день будет присылать 1 интересный фильм или сериал с описанием в выбраном жанре.\n"
        "\n/topfilms - запрос топ картин в выбранном жанре.\n"
        "\nБот составляет список лучших или худших по рейтингу картин в выбранных категориях.\n"
        "\n/film - запрос информации о картине по названию.\n"
        "\nБот выводит информацию о картине, название которой вы напишете в сообщении.\n"
        "\n/history - история ваших запросов боту.\n"
        "\n/help - информация по боту."
    )
