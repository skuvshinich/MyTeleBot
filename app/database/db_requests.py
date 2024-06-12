from app.database.models import async_session
from app.database.models import User, UserRequest, CreateFilm, UserFilm
from sqlalchemy import select
from datetime import datetime
from typing import Any

import random

from app.utils import open_url


async def set_user(tg_id: int, name: str) -> None:
    """
    Функция сохраняет данные пользователя в базу данных.

    :param tg_id: Telegram ID пользователя.
    :param name: Имя пользователя в Telegram.

    :return:
    None
    """

    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, name=name))
            await session.commit()


async def save_request(tg_id: int, req_name: str, req_time: datetime) -> None:
    """
    Функция сохраняет данные запроса пользователя в боте.

    :param tg_id: Telegram ID пользователя.
    :param req_name: Название команды.
    :param req_time: Датта и время сделанного запроса.

    :return:
    None
    """

    async with async_session() as session:
        session.add(UserRequest(tg_id=tg_id, request=req_name, created_time=req_time))
        await session.commit()


async def show_history(tg_id: int) -> str:
    """
    Функция выбирает из базы данных запросы пользователя по его Telegram ID,
    и форматирует их в строку.

    :param tg_id: Telegram ID пользователя.

    :return:
    Возвращает историю запросоав пользователя в виде строки.
    """

    async with async_session() as session:
        requests = await session.scalars(
            select(UserRequest).filter(UserRequest.tg_id == tg_id)
        )
        response = ""
        for req in requests:
            request_str = f'\nЗапрос {req.request} выполнен {datetime.strftime(req.created_time, "%Y-%m-%d в %H:%M")}'
            response += request_str
            # print(request_str)

        return response


async def create_notice(tg_id: int, genre: str, time: str) -> None:
    """
    Функция вносит данные о выбранном жанре и времени в базу данных, когда пользователь подключает
    ежедневную отрпавку интересных фильма или сериалов.
    Если пользователь вносит данные не первый раз, то функция меняет их на новые.

    :param tg_id: Telegram ID пользователя.
    :param genre: Выбранный пользователем жанр.
    :param time: Выбранное пользователем время.

    :return:
    None
    """

    async with async_session() as session:
        notice = await session.scalar(
            select(CreateFilm).filter(CreateFilm.tg_id == tg_id)
        )

        if not notice:
            session.add(CreateFilm(tg_id=tg_id, genre=genre, notice_time=time))
            await session.commit()
        else:
            replace = session.get(CreateFilm, tg_id)
            replace.genre, replace.time = genre, time
            await session.commit()


async def save_film(tg_id: int, film: str) -> None:
    """
    Функция вносит фильм, отрпавленный пользователю в ежедневной рассылке, в базу данных,
    чтобы этот фильм не был отрпавлен пользователю еще раз.

    :param tg_id: Telegram ID пользователя.
    :param film: Название фильма.

    :return:
    None
    """

    async with async_session() as session:
        session.add(UserFilm(tg_id=tg_id, film_name=film))
        await session.commit()


async def get_films_from_db(tg_id: int) -> list:
    """
    Функция выбирает по Telegram ID пользователя фильмы, которые уже были отправлены
    в ежедневной рассылке и формирует из них список.

    :param tg_id: Telegram ID пользователя.

    :return:
    Список фильмов, которые уже были отправлены пользователю в ежедневной рассылке.
    """

    async with async_session() as session:
        films = await session.scalars(select(UserFilm).filter(UserFilm.tg_id == tg_id))
        films_list = [film.film_name for film in films]

        return films_list


async def get_film(tg_id: int, genre: str) -> Any:
    """
    Получает фильмы с хорошим рейтингом, формирует список их имен, выбирает один рандомный и
    проверяет не отрпавлялся ли он уже пользователю.

    :param tg_id: Telegram ID пользователя.
    :param genre: Выбранный пользователем жанр.

    :return:
    Возвращает данные, полученные из URL-адреса в формате JSON.
    """

    films = await get_films_from_db(tg_id)

    url = f"https://api.kinopoisk.dev/v1.4/movie?page=1&limit=250&selectFields=name&rating.kp=7-10&genres.name={genre}"
    file = open_url(url)
    api_res = [film["name"] for film in file["docs"]]

    while True:
        user_film = random.choice(api_res)

        if user_film not in films:
            await save_film(tg_id, user_film)
            return await get_film_info(user_film)


async def get_film_info(user_film):
    """
    Функция получает от пользователя название, делает request к API по названию,
    получает JSON файл, берет оттуда ID фильма, делает по нему request и полученные данные возвращает.

    :param user_film: Название фильма или сериала.

    :return:
    Возвращает данные о фильме в формате JSON.

    P.S. Делаю 2 запроса, т.к. в JSON-файле, полученном запросом по названию, информации о кинокартине меньше,
    чем полученном зопросом по ID фильма.
    """

    name_url = (
        f"https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=1&query={user_film}"
    )
    name_file = open_url(name_url)

    # with open('test1.json', 'w', encoding='utf8') as tst:
    #     json.dump(name_file, tst, ensure_ascii=False, indent=4)

    film_id = name_file["docs"][0]["id"]

    id_url = f"https://api.kinopoisk.dev/v1.4/movie/{film_id}"

    res_file = open_url(id_url)

    # with open('../../test2.json', 'w', encoding= 'utf8') as tst:
    #      json.dump(res_file, tst, ensure_ascii=False, indent=4)

    return res_file
