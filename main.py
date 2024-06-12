import asyncio

# import logging

from loader import bot, dp
from commands_hendlers import router as main_router
from app.database.models import create_db


async def main() -> None:
    """
    Функция создает базу данных, подключает все роутеры к диспетчеру и запускает телеграм-бота.

    :return:
    None
    """
    await create_db()
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")
