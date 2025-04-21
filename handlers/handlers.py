import logging
import asyncio
import kb.keyboards as kb
from words import words as w
from db.database import DataBase
from states import states as st

from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, or_f, StateFilter


logger = logging.getLogger(__name__)
rt = Router()
db = DataBase()


asyncio.get_event_loop().run_until_complete(db.create_pool())
asyncio.get_event_loop().run_until_complete(db.create_tables())


@rt.startup()
async def inform_start_bot():
    logger.info('Router started')
    print('Bot started')


@rt.message(Command('start', 'help'))
async def start_bot(message: Message, state: FSMContext):
    await db.add_user(chat_id=message.from_user.id,
                username=message.from_user.username,
                full_name=message.from_user.full_name)
    await state.clear()
    await message.answer(text=w.start_text, reply_markup=kb.start_markup)
