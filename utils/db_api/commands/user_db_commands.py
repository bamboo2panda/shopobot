from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User


async def add_user(user_id: int, name: str, email: str = None, referral: int = None, balance: int = 0):
    try:
        if referral:
            user = User(user_id=user_id, name=name, email=email, referral=referral, balance=balance)
            await user.create()
            referral = await User.get(referral)
            await referral.update(ballance=User.balance+10).apply()
        else:
            pass
        # Обработка без реферала
    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(user_id: int):
    user = await User.query.where(User.id == user_id).gino.first()
    return user


async def select_users_ids():
    ids = await User.query.select(User.id).gino.all()
    return ids


async def count_users():
    total = await db.func.count(User.user_id).gino.scalar()
    return total


async def update_user_email(user_id, email):
    user = await User.get(user_id)
    await user.update(email=email).apply()
