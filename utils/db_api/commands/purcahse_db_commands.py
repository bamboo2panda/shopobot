from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.purchase import Purchase


async def add_purchase(user_id: int,
                       item_id: int,
                       transaction_id: str,
                       count: int,
                       address: str,
                       points_used: int,
                       amount: int):
    try:
        purchase = Purchase(user_id=user_id,
                            item_id=item_id,
                            transaction_id=transaction_id,
                            count=count,
                            address=address,
                            points_used=points_used,
                            amount=amount)
        await purchase.create()
    except UniqueViolationError:
        pass
