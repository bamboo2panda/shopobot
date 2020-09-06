from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.item import Item


async def add_item(name: str, description: str, photo: str = None, price: int = 0):
    try:
        item = Item(photo=photo, name=name, description=description, price=price)
        await item.create()
    except UniqueViolationError:
        pass


async def select_all_items():
    items = await Item.query.gino.all()
    return items


async def select_user(item_id: int):
    item = await Item.query.where(Item.id == item_id).gino.first()
    return item


async def count_items():
    total = await db.func.count(Item.id).gino.scalar()
    return total


async def update_user_email(user_id, email):
    user = await Item.get(user_id)
    await user.update(email=email).apply()
