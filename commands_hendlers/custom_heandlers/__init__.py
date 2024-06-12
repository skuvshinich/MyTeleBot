__all__ = ("router",)

from aiogram import Router

from .kino_daily import router as notice_router
from .history import router as history_router
from .top_films import router as top_films_router
from .film_info import router as film_router
from .cancel_heandler import router as cancel_router

router = Router(name=__name__)

router.include_routers(
    notice_router, history_router, top_films_router, film_router, cancel_router
)
