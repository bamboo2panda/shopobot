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


async def select_item(item_id: int):
    item = await Item.query.where(Item.id == item_id).gino.first()
    return item


async def count_items():
    total = await db.func.count(Item.id).gino.scalar()
    return total


async def search_item_by_name(name: str):
    search = "%{}%".format(name)
    result = await Item.query.where(Item.name.like(search)).gino.all()
    return result


async def get_item_price(id: int):
    points_object = await Item.query.with_only_columns(Item.price).where(Item.id == id).gino.first()
    return points_object.__values__["price"]

