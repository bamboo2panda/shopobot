from sqlalchemy import Column, BigInteger, String, sql, Integer
from utils.db_api.db_gino import TimeBaseModel


class User(TimeBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    balance = Column(Integer)
    referral = Column(BigInteger)

    query: sql.Select
