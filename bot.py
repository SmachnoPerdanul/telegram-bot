import asyncio
import logging
import os
import requests

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_price(coin_id: str):
    params = {"ids": coin_id, "vs_currencies": "usd"}
    response = requests.get(COINGECKO_URL, params=params, timeout=10)
    data = response.json()
    return data[coin_id]["usd"]

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Я твой первый бот.")

@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("Чем могу помочь?")

@dp.message(Command("price"))
async def price_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Bitcoin", callback_data="price_bitcoin")],
        [InlineKeyboardButton(text="Ethereum", callback_data="price_ethereum")],
    ])
    await message.answer("Выбери монету:", reply_markup=keyboard)
    
@dp.callback_query(F.data.startswith("price_"))
async def price_callback(callback: CallbackQuery):
    coin_id = callback.data.split("_")[1]
    price = get_price(coin_id)
    await callback.message.answer(f"{coin_id.capitalize()}: {price} USD")
    await callback.answer()

@dp.message()
async def echo_handler(message: Message):
    await message.answer(f"Ты написал: {message.text}")

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())