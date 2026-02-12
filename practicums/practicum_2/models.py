from datetime import datetime, date, UTC
from decimal import Decimal

# from sqlalchemy import Integer, String, Float, UniqueConstraint, DateTime, ForeignKey, Date, Numeric
# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
#
# from practicums.practicum_2.database_connection import engine
#
#
# class Base(DeclarativeBase):
#     __abstract__ = True
#
#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True,
#         unique=True,
#         autoincrement=True,
#     )
#
#
# class Mineral(Base):
#     __tablename__ = "minerals"
#
#     name: Mapped[str] = mapped_column(String(50), unique=True)
#     color: Mapped[str] = mapped_column(String(30))
#     hardness: Mapped[float] = mapped_column(Float)
#
#     # # Связи
#     # shipments: Mapped[list["Shipment"]] = relationship(back_populates="mineral")
#     # prices: Mapped[list["Price"]] = relationship(back_populates="mineral")
#     #
#
# class Salon(Base):
#     __tablename__ = "salons"
#     __table_args__ = (  # эта настройка помогает задать дополнительные конфигурации таблицы
#         UniqueConstraint("name", "location"),  # а тут мы говорим: сочетание названия салона и его адреса должно быть уникальным
#     )
#
#     name: Mapped[str] = mapped_column(String(50))
#     location: Mapped[str] = mapped_column(String(100))

    # # Связи
    # employees: Mapped[list["Employee"]] = relationship(back_populates="salon")
    # shipments_details: Mapped[list["SalonShipmentAssociation"]] = relationship(
    #     back_populates="salon",
    #     cascade="all, delete-orphan",
    # )
    # shipments = association_proxy("shipments_details", "shipment")
    #
# ==================== TASKS ================================

from datetime import datetime, date, UTC
from decimal import Decimal

from sqlalchemy import Integer, String, Float, UniqueConstraint, DateTime, ForeignKey, Date, Numeric
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from practicums.pr_2.database_connection import engine


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )


# ТЕХНИЧЕСКОЕ ЗАДАНИЕ:
# Создать модель минерала для системы управления поставками драгоценных камней.
#
# ТРЕБОВАНИЯ:
# - Уникальный идентификатор (BigInteger, автоинкремент)
# - Название минерала (строка, максимум 50 символов, уникальное)
# - Цвет минерала (строка, максимум 30 символов)
# - Твердость по шкале Мооса (число с плавающей точкой)
#
# ЦЕЛЬ: Создать основу для каталога минералов, которые будут поставляться в салоны.


from decimal import Decimal

from flask import Config
from pydantic import BaseModel, ConfigDict
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


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )



class Mineral(Base):
    __tablename__ = "minerals"

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



# ТЕХНИЧЕСКОЕ ЗАДАНИЕ:
# Создать модель салона для системы управления сетью элитных бутиков.
#
# ТРЕБОВАНИЯ:
# - Уникальный идентификатор
# - Название салона (строка, максимум 50 символов)
# - Местоположение салона (строка, максимум 100 символов)
# - Ограничение уникальности: комбинация (название + местоположение) должна быть уникальной
#
# ЦЕЛЬ: Создать систему управления салонами, куда будут доставляться минералы.


class Salon(Base):
    __tablename__ = "salons"
    __table_args__ = (
        UniqueConstraint("name", "address"),)

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    address: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )


Base.metadata.create_all(engine)