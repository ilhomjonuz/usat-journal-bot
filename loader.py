from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage


from data import config
from utils import CertificateGenerator

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
generator = CertificateGenerator(
    template_path="license/license.jpg",
    font_path="fonts/BelgianoSerif2.ttf"
)
