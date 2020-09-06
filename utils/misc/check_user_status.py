from data.config import super_admins as sa


async def is_product_admin(user_id: int):
    print(sa)
    if str(user_id) in sa:
        return True
    return False
