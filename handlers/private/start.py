from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import BotAdminFilter
from keyboards.reply import admin_menu
from loader import dp


@dp.message(CommandStart(), BotAdminFilter())
async def admin_start(message: Message, state: FSMContext):
    await message.answer(f"Bosh sahifa", reply_markup=admin_menu)
    await state.clear()
