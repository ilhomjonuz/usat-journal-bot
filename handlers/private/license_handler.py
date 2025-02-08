import asyncio
from token import AWAIT

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile

from filters import BotAdminFilter
from keyboards.reply import admin_menu
from loader import dp
from states import LicenseStates
from utils import generate_license


@dp.message(BotAdminFilter(), F.text == "🎓 Guvohnoma uchun sertifikat")
async def license_certificate(msg: Message, state: FSMContext):
    await msg.answer("Guvohnoma oluvchining ism-familiyasini yuboring:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(LicenseStates.fullname)


@dp.message(LicenseStates.fullname, F.text)
async def license_get_fullname(msg: Message, state: FSMContext):
    await state.update_data({'full_name': msg.text})
    await msg.answer("Yo‘nalishni yuboring:")
    await state.set_state(LicenseStates.direction)


@dp.message(LicenseStates.direction, F.text)
async def license_get_direction(msg: Message, state: FSMContext):
    await state.update_data({'direction': msg.text})
    await msg.answer("O‘quv yilini quyidagi formatda yuboring:\n\n<code>2024/2025</code>")
    await state.set_state(LicenseStates.academic_year)


@dp.message(LicenseStates.academic_year, F.text.regexp(r"^(20\d{2})/(20\d{2})$"))
async def license_get_academic_year(msg: Message, state: FSMContext):
    first_year, last_year = msg.text.split('/')
    await state.update_data({'academic_year_first': first_year, 'academic_year_last': last_year})
    await msg.answer("Guvohnoma sanasining yilini quyidagi formatda yuboring:\n\n<code>2025</code>")
    await state.set_state(LicenseStates.date)


@dp.message(LicenseStates.date, F.text.regexp(r"^20\d{2}"))
async def license_get_date(msg: Message, state: FSMContext):
    await state.update_data({'date_year': msg.text})
    await msg.answer("Guvohnoma sanasining kunini quyidagi formatda yuboring:\n\n<code>7 fevral</code>")
    await state.set_state(LicenseStates.date_month)


@dp.message(LicenseStates.date_month)
async def license_get_date_month(msg: Message, state: FSMContext):
    await state.update_data({'date_month': msg.text})
    await msg.answer("Buyrug‘ sonini yuboring")
    await state.set_state(LicenseStates.order_number)


@dp.message(LicenseStates.order_number, F.text.regexp(r"^\d+$"))
async def license_get_order_number(msg: Message, state: FSMContext):
    await state.update_data({'order_number': msg.text})
    data = await state.get_data()
    await state.clear()
    resp = await generate_license(**data)
    if resp['ok']:
        await_msg = await msg.answer("⏳ Guvohnoma tayyorlanmoqda...")
        cert_image = FSInputFile(resp['data'])
        await msg.answer_document(cert_image, reply_markup=admin_menu)
        await await_msg.edit_text("✅ Guvohnoma muvaffaqiyatli yuborildi.")
    else:
        await msg.answer(resp['error'], reply_markup=admin_menu)


@dp.message(StateFilter(LicenseStates))
async def error_choice_group(message: Message):
    await message.delete()
    warning_msg = await message.answer("❌ Iltimos, ma’lumotni to‘g‘ri yuboring!")
    await asyncio.sleep(3)
    await warning_msg.delete()
