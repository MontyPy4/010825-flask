"""ТЕХНИЧЕСКОЕ ЗАДАНИЕ:
Создать модель минерала для системы управления поставками драгоценных камней.

ТРЕБОВАНИЯ:
- Уникальный идентификатор (BigInteger, автоинкремент)
- Название минерала (строка, максимум 50 символов, уникальное)
- Цвет минерала (строка, максимум 30 символов)
- Твердость по шкале Мооса (число с плавающей точкой)

ЦЕЛЬ: Создать основу для каталога минералов, которые будут поставляться в салоны."""

from decimal import Decimal
from enum import unique

from sqlalchemy import (create_engine,
                        Numeric ,
                        BigInteger,
                        Column,
                        String,
                        SmallInteger,
                        Boolean,
                        Integer,
                        ForeignKey)
from sqlalchemy.orm import (sessionmaker,
                            DeclarativeBase,
                            Mapped,
                            mapped_column,
                            relationship)
from pathlib import Path

class Base(DeclarativeBase):       # абстрактный класс
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,    # уникальный id
        autoincrement=True   # автозаполнение
    )

class Minneral(Base):
    __tablename__ = 'minerals'

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    color: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    hardness: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable=False
    )

engine =create_engine("sqlite:///minerals.db")   # помогает создать подключение к базе с которой  будем работать
Base.metadata.create_all(engine)