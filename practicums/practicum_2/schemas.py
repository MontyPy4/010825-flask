from pydantic import BaseModel, ConfigDict
from sqlalchemy import DECIMAL


class MineralOut(BaseModel):
    model_config = ConfigDict(  # эта настройка помогает задать дополнительные конфигурации модели
        from_attributes=True,  # поможет пайдантик работать с классами и их аттрибутами
        str_strip_whitespace=True,  # для всех строковых полей убирает пробелы
        extra="forbid"  # запрещает создание полей, которых нет в модели
    )

    id: int
    name: str
    color: str
    hardness: DECIMAL


# ==================== TASKS =================

# Создать Pydantic схему для безопасного вывода информации о минералах в API.
#
# ТРЕБОВАНИЯ:
# - Валидация всех полей модели Mineral
# - Поддержка сериализации из SQLAlchemy объектов
# - Готовность к использованию в FastAPI/Flask endpoints
#
# ЦЕЛЬ: Обеспечить типобезопасность и валидацию при передаче данных о минералах.

class MineralOutput(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    id: int
    name: str
    color: str
    solid: DECIMAL


mineral = {"id":3, "name": "gold", "color": "yellow", "solid": 1234.43}

resp =MineralOutput.model_validate(mineral)
print(resp)
