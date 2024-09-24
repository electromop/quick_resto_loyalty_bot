import asyncio
import logging

from handlers import common, register, bonus_extended, admin

from api import app
import uvicorn
from extensions import bot, dp


# async def start_uvicorn():
#     config = uvicorn.Config(app, host="0.0.0.0", port=8081)
#     server = uvicorn.Server(config)
#     await server.serve()

async def start_bot():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp.include_routers(common.router, register.router, bonus_extended.router, admin.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # asyncio.gather(main(), start_uvicorn())
    asyncio.run(start_bot())