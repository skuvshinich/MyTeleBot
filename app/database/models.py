from typing import Annotated
from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime

from config_data.config import SQL_URL


engine = create_async_engine(url=SQL_URL)
async_session = async_sessionmaker(engine)


intpk = Annotated[int, mapped_column(primary_key=True)]
bigint = Annotated[int, mapped_column(BigInteger)]
str25 = Annotated[str, mapped_column(String(25))]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    tg_id: Mapped[bigint]
    name: Mapped[str25]
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class UserRequest(Base):
    __tablename__ = "requests"

    id: Mapped[intpk]
    tg_id: Mapped[bigint]
    request: Mapped[str25]
    created_time: Mapped[datetime] = mapped_column(DateTime)


class UserFilm(Base):
    __tablename__ = "films"

    id: Mapped[intpk]
    tg_id: Mapped[bigint]
    film_name: Mapped[str25]


class CreateFilm(Base):
    __tablename__ = "movie_every_day"

    id: Mapped[intpk]
    tg_id: Mapped[bigint]
    genre: Mapped[str25]
    notice_time: Mapped[str25]


async def create_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
