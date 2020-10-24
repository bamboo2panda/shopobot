from asyncpg import UniqueViolationError
from sqlalchemy import text, column

from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User


async def add_user(id: int, name: str, email: str = None, referral: int = None, balance: int = 0):
    try:
        if referral:
            user = User(id=id, name=name, email=email, referral=referral, balance=balance)
            await user.create()
            referral = await User.get(referral)
            await referral.update(balance=User.balance+10).apply()
        else:
            pass
        # Обработка без реферала
    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def select_users_ids():
    ids_objects = await User.query.with_only_columns([User.id]).gino.all()
    ids = []
    for id in ids_objects:
        ids.append(id.__values__["id"])
    print(ids)
    return ids


async def get_user_points(id: int):
    points_object = await User.query.with_only_columns(User.balance).where(User.id == id).gino.first()
    return points_object.__values__["balance"]


async def count_users():
    total = await db.func.count(User.id).gino.scalar()
    return total


async def update_user_email(id, email):
    user = await User.get(id)
    await user.update(email=email).apply()


async def cut_points(user_id, amount):
    User.update()
