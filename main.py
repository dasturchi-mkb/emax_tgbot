import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from config.config import BOT_TOKEN
from handlers import handlers


logger = logging.getLogger(__name__)
logging.basicConfig(
                    filename='logs/log.log',
                    filemode='a',
                    format=u'%(filename)+13s [ LINE:%(lineno)-.4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG)


async def set_commands(bot: Bot):

    bot_commands = [
        BotCommand(command='/start', description='📜 Главное меню'),
        BotCommand(command='/stats', description = '📊 Статистика'),
    ]
    await bot.set_my_commands(bot_commands)


async def main():
    session = AiohttpSession(proxy='http://172.23.11.105:2002')
    bot = Bot(token=BOT_TOKEN,
              default=DefaultBotProperties(parse_mode='html'),
              session=session)

    dp = Dispatcher(storage=MemoryStorage())
    await set_commands(bot)
    dp.include_router(handlers.rt)
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print('Goodbye')
        asyncio.run(dp.stop_polling())


if __name__ == '__main__':
    asyncio.run(main())
