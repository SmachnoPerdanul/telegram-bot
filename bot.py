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


def get_price(coin_id: str, vs_currency: str):
    params = {"ids": coin_id, "vs_currencies": vs_currency}
    response = requests.get(COINGECKO_URL, params=params, timeout=10)
    data = response.json()
    return data[coin_id][vs_currency]

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
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="USD", callback_data=f"show_{coin_id}_usd")],
        [InlineKeyboardButton(text="RUB", callback_data=f"show_{coin_id}_rub")],
    ])
    await callback.message.answer("Выбери валюту:", reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(F.data.startswith("show_"))
async def show_callback(callback: CallbackQuery):
    coin_id = callback.data.split("_")[1]
    vs_currency = callback.data.split("_")[2]
    price = get_price(coin_id, vs_currency)
    await callback.message.answer(f"{coin_id.capitalize()}: {price} {vs_currency.upper()}")
    await callback.answer()

@dp.message()
async def echo_handler(message: Message):
    await message.answer(f"Ты написал: {message.text}")

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())