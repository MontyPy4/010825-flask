from flask import Flask

from core.config import settings
from core.db import db


def init_database(app: Flask): # инициализация базы данных
    db.init_app(app)

def register_routes(app: Flask): # регистрация маршрутов
    ...

def crete_app(app: Flask): # создание приложения
    app.config.update(settings.get_flask_config())  # словарь - объект с методами

    init_database(app)
    register_routes(app)

    return app


