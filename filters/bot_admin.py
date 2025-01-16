from aiogram import filters
from aiogram.types import Message, CallbackQuery

from data.config import ADMINS


class BotAdminFilter(filters.BaseFilter):

    async def __call__(self, obj: [Message, CallbackQuery], *args, **kwargs):
        if isinstance(obj, CallbackQuery):
            obj = await obj.message
        return obj.chat.type == 'private' and f'{obj.from_user.id}' in ADMINS
