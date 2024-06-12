from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def Reply_kb_builder(words_list, *args) -> ReplyKeyboardMarkup:
    """
    Функция для создания ReplyKeyboard.

    :param words_list: список из слов для кнопок клавиатуры
    :param args: разметка клавиатуры

    :return:
    ReplyKeyboardMarkup: возвращает реплай клавиатуру с определенной разметкой.
    """
    builder = ReplyKeyboardBuilder()
    for word in words_list:
        builder.add(KeyboardButton(text=word))
    builder.adjust(*args)
    result = builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберете пункт меню",
        one_time_keyboard=True,
    )

    return result


word_list = ["лучшие", "худшие", "/cancel❌"]
keyboard1 = Reply_kb_builder(word_list, 2, 1)

nums_top = ["5", "10", "25", "/cancel❌"]
keyboard2 = Reply_kb_builder(nums_top, 3, 1)

movie_types = ["фильмы", "сериалы", "мультфильмы", "мультсериалы", "аниме", "/cancel❌"]
keyboard3 = Reply_kb_builder(movie_types, 1, 2, 2, 1)

genres = [
    "все жанры",
    "комедия",
    "мелодрама",
    "драма",
    "ужасы",
    "триллер",
    "боевик",
    "детектив",
    "фантастика",
    "документальный",
    "детский",
    "криминал",
    "мюзикл",
    "спорт",
    "вестерн",
    "/cancel❌",
]
keyboard4 = Reply_kb_builder(genres, 1, 3, 3, 3, 3, 3, 1)

sites = ["Kinopoisk", "IMDb", "/cancel❌"]
keyboard5 = Reply_kb_builder(sites, 2, 1)

keyboard6 = Reply_kb_builder(genres[1:], 2, 3, 3, 3, 3, 1)
