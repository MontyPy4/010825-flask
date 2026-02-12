from sqlalchemy import create_engine, select, or_, not_, and_, desc, func
from sqlalchemy.orm import sessionmaker, aliased

from sqlalchemy_lessons.lesson_2.db_connector import DBConnector
from sqlalchemy_lessons.lesson_2.social_blogs_models import *

engine = create_engine(
    url="mysql+pymysql://ich1:ich1_password_ilovedbs@ich-edit.edu.itcareerhub.de:3306/social_blogs",
    echo=True,
    future=True
)


# Session = sessionmaker(bind=engine)
# session = Session()
# session.close()


with DBConnector(engine) as session:
    # CRUD operations

    # C (Create)
    data = {"name": "NewRole"}

# С (Create

    new_role = Role(**data)

    session.add(new_role) # Add the new role to the session
    session.commit() # Commit the transaction

# R (Read)
# Read one object

user = session.get(User, 11)  # 11 - id
print(user) # объект пользователя

#print(user.email)
print(user.first_name)
print(user.last_name)

# # Read all objects
# # stmt (STATEMENT) - Сырой SQL запрос
# all_authors = (
#     select(User.email, User.first_name, User.last_name) # SELECT * FROM 'user'
#     .where(User.role_id == 3)  # вызов фильтрации - WHERE role_id = 3
# )
#
# # запуск запроса
# # По умолчанию вернётся [Row(User()), Row(User())...]
# # Чтобы вернулся читабельный объект, нужно использовать scalars()
# response = session.execute(all_authors).scalars() # аналог курсор
# print(response.all())
#
# data = [{
#     "id": user.id,
#     "name": user.name,
#     "last_name": user.last_name,
#     "role": user.role.name
#     }
#     for user in response
#     ]
# print(data)

# Read many
all_authors = (  # stmt (STATEMENT)
    select(User)  # SELECT * FROM `user`
    .where(User.role_id == 3) # WHERE role_id = 3
)

# по умолчанию вернётся [Row(User()), Row(User()), ..., Row(User())]
response = session.execute(all_authors).scalars() # -> [User(), User(), ..., User()]

data = [
    {
        "id": user.id,
        "name": user.first_name,
        "role": user.role_id
    }
    for user in response
]


print(data)

# Получить только пользователей старше 30

res = session.query(User).filter(User.rating > 5).all()

# v2
# С начала создаем состояние
stmt = (
    select(User)
    .where(User.rating > 5)
)
# Инициализируем подключение
res = session.execute(stmt).scalars()

for obj in res:
    print(obj.email, obj.rating)


# Like(), between(), in()
# Вывод фамилий на букву "М"

stmt = (
    select(User)
    .where(User.last_name.like("M%"))  # last_name - маппированая колонка типа данных str
)

result = session.execute(stmt).scalars()

print(result)

for user in result:
    print(user.last_name, user.role_id)


# Посмотреть рейтинг

stmt = (
    select(User)
    .where(User.rating.between(2,5))
)
res = session.execute(stmt).scalars()
# execute - по умолчанию возвращает кортеж, а scalars - убирает лишнюю вложенность - возьми у каждой строки первую колонку
for row in res:
    print(row.rating)


# Or_, not_, and_

# взять только авторов с рейтингом больше 6

stmt = (
    select(User)
        .where(
        and_(User.role_id==3, User.rating > 6)
    )
    .order_by(desc(User.rating))  # по умолчанию сортировка ascending / чтобы сделать desc - нужен импорт
)

res = session.execute(stmt).scalars()

for  user in res:
    print(user.rating, user.role_id)


# Сортировку можно делать по нескольким полям (максимум по 3-м)
# Все объекты которые найдены будут сперва сортироваться по рейтингу, а после по букве фамилии

stmt = (
    select(User)
    .where(
        and_(User.role_id == 3, User.rating > 6)
    )
    .order_by(desc(User.rating), User.last_name)
)

res = session.execute(stmt).scalars()

for user in res:
    print(user.rating, user.last_name)


# =================================================
# Агрегации и группировки
# Group_by
# Необходимо импорт класс func

# Пример 1: Средний рейтинг пользователей

stmt = (  # указываю свою новую колонку
    select(func.avg(User.rating))                       # SELECT AVG('user'.rating) FROM user;
)

res =  session.execute(stmt).scalar()

# print(res)   # Вывод без scalar() : ChunkedIteratorResult object at 0x00000140BE688A10>
print(res)


# Если после запроса это один объект но много колонок - scalars
# Если после запроса это объединение одного значения (глобальная группировка)- scalar

# ======= Если нужно сделать группировку по пользователям и для каждой группы сделать свой рейтинг
# Scalars - забирает первую запись с одной колонки
# SELECT user.role_id, AVG(user.rating)
# FROM user
# GROUP BY user.role_id;

stmt = (
    select(User.role_id, func.avg(User.rating))  # SELECT user.role_id, AVG('user'.rating) FROM user GROUP BY uer.role_id;
    .group_by(User.role_id)
)

result = session.execute(stmt).scalars()

print(result)

for res in result:
    print(res)

# ==============================ALIAS - псевдоним =================================================

# Требует импорт from sqlalchemy.orm import sessionmaker, aliased

# us = alias(selectable=User,name="us") # us - сам псевдоним
us = aliased(element=User, name="us")

# Посмотреть как много людей под одной группой
# С ГРУППИРОВКА ИСПОЛЬЗУЕМ ALL


us = aliased(element=User, name="us")


stmt = (
    select(
        us.role_id,
        func.count(us.id).label("count_of_users")   # "count)of_users" название сгруппированной колонки
    )
    .group_by(us.role_id)
)

result = session.execute(stmt).all() #  получаем список с кортежами -> [1, 1), (2, 4), (3, 26)]

for group_ in result:
    print(f"user role: {group_.role_id}  | Count of Users: {group_.count_of_users}")


# ============ HAVING - второй уровень - фильтрация после группировки ===========
# На момент составления запроса Работа с .label запрещена: ("count_of_users")

us = aliased(element=User, name="us")

stmt = (
    select(
        us.role_id,
        func.count(us.id).label("count_of_users")
    )
    .group_by(us.role_id)
    .having(func.count(us.id) > 4)
)

result = session.execute(stmt).all() # -> [(3, 26)]

for group_ in result:
    print(f"user role: {group_.role_id}  | Count of Users: {group_.count_of_users}")


# Получить средний рейтинг только по авторам

# mean_rete_by_author_sql = select(
#     func.avg(User.rating).label("User_rating")
# .where(User.role_id == 3).scalar_subquery()

# main_query = select(User).where(User.rating > mean_rate_by_author_sbq)
# )

