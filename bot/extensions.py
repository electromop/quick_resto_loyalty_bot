from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import Config
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(Config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
db = create_async_engine(Config.DATABASE_URL)

Session = async_sessionmaker(bind=db, expire_on_commit=False)

# def make_session():
#     db = Session
#     try:
#         yield db
#     finally:
#         db.close()

from quick_resto_API import quick_resto_interface as qri

qri_sdk = qri.QuickRestoInterface(login=Config.QUICK_RESTO_API_USERNAME,
                                password=Config.QUICK_RESTO_API_PASSWORD)
