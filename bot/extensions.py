from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import Config

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(Config.BOT_TOKEN)
db = create_async_engine(Config.DATABASE_URL)
Session = async_sessionmaker(bind=db)
