from aiogram import types, F
from aiogram.fsm.state import State

from filters import PrivateFilter
from keyboards.reply import admin_menu
from loader import dp


@dp.message(PrivateFilter(), State(), F.text == "🔙 Orqaga")
async def bad_message(message: types.Message):
    await message.answer("Bosh sahifa", reply_markup=admin_menu)

# Echo bot
@dp.message(PrivateFilter(), State())
async def bot_echo(message: types.Message):
    await message.answer(message.text)


@dp.callback_query(PrivateFilter(), State())
async def bad_callback_query(call: types.CallbackQuery):
    await call.message.edit_text("Xabar o'chirildi.")
