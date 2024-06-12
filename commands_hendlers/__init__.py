from aiogram import Router

from .custom_heandlers import router as custom_router
from .default_heandlers import router as default_router

router = Router(name=__name__)

router.include_router(custom_router)
router.include_router(default_router)
