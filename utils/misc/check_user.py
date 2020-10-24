from data.config import super_admins as sa
from aiogram import types

from utils.db_api.commands import user_db_commands as commands


async def is_product_admin(user_id: int):
    print(sa)
    if str(user_id) in sa:
        return True
    return False


async def is_registered_user(user_id: int):
    user_ids = await commands.select_users_ids()
    # if user_id in user_ids or user_id in sa:
    if user_id in user_ids:
        return True
    return False


async def check_referral(referral):
    user_ids = await commands.select_users_ids()
    if referral in user_ids:
        return True
    else:
        return False
