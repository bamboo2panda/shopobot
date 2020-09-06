from sqlalchemy import Column, BigInteger, String, sql, Integer, Text
from utils.db_api.db_gino import TimeBaseModel


class Item(TimeBaseModel):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(Text)
    photo = Column(String(255))
    price = Column(Integer)

    query: sql.Select
