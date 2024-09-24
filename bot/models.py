import asyncio

from sqlalchemy import Column, BigInteger, Integer, String, Enum, Time, ForeignKey, Boolean, Date, Text, Interval, MetaData, DateTime
from sqlalchemy.ext.declarative import declarative_base

from extensions import db

Base = declarative_base()

class BotUser(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, nullable=False)
    quick_resto_id = Column(Integer, unique=True, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    phone = Column(String, nullable=True)
    is_admin = Column(Boolean, nullable=True, default=False)

async def create_tables():
    async with db.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())