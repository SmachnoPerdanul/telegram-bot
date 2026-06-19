import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Я твой первый бот.")

@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("Чем могу помочь?")

@dp.message()
async def echo_handler(message: Message):
    await message.answer(f"Ты написал: {message.text}")

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())