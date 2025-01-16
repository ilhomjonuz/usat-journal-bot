from aiogram import filters
from aiogram.types import Message, CallbackQuery


class PrivateFilter(filters.BaseFilter):

    async def __call__(self, obj: [Message, CallbackQuery], *args, **kwargs):
        if isinstance(obj, CallbackQuery):
            obj = await obj.message
        return obj.chat.type == 'private'
