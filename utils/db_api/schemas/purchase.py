from sqlalchemy import Column, BigInteger, String, sql, Integer, Text
from utils.db_api.db_gino import TimeBaseModel


class Purchase(TimeBaseModel):
    __tablename__ = 'purchase'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer)
    item_id = Column(Integer)
    transaction_id = Column(String)
    count = Column(Integer)
    address = Column(Text)
    points_used = Column(Integer)
    amount = Column(Integer)

    query: sql.Select