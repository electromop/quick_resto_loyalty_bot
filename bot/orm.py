from typing import Optional
from sqlalchemy import select
from extensions import Session
from models import BotUser

class BotUserManager:
    def __init__(self):
        self.session = Session()

    async def add(self, user: BotUser) -> BotUser:
        self.session.add(user)
        await self.session.commit()
        await self.session.close()
        return user

    async def get(self, user_id: int) -> Optional[BotUser]:
        user = await self.session.get(BotUser, user_id)
        return user

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[BotUser]:
        statement = select(BotUser).where(BotUser.telegram_id == telegram_id)
        result = await self.session.execute(statement)
        await self.session.close()
        return result.scalars().first()

    async def get_all(self) -> list[BotUser]:
        statement = select(BotUser)
        result = await self.session.execute(statement)
        await self.session.close()
        return result.scalars().all()

    # async def filter_by(self, **filters) -> list[BotUser]:
    #     await self.session.query(BotUser).filter_by(**filters).all()

    async def delete(self, user: BotUser) -> bool:
        try:
            self.session.delete(user)
            await self.session.commit()
            await self.session.close()
            return True
        except:
            await self.session.close()
            return False

