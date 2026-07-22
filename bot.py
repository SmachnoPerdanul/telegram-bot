import asyncio
import logging
import os
import requests

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from dotenv import load_dotenv

from database import init_db, add_favorite, get_favorites, remove_favorite

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_price(coin_id: str, vs_currency: str):
    params = {"ids": coin_id, "vs_currencies": vs_currency}
    try:
        response = requests.get(COINGECKO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data[coin_id][vs_currency]
    except requests.exceptions.RequestException as error:
        logging.error(f"Ошибка запроса к API: {error}")
        return None
    except (KeyError, ValueError) as error:
        logging.error(f"Неожиданный ответ API: {error}")
        return None


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Я твой первый бот.")


@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("Чем могу помочь?")


@dp.message(Command("price"))
async def price_handler(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Bitcoin", callback_data="price_bitcoin")],
            [InlineKeyboardButton(text="Ethereum", callback_data="price_ethereum")],
        ]
    )
    await message.answer("Выбери монету:", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("price_"))
async def price_callback(callback: CallbackQuery):
    coin_id = callback.data.split("_")[1]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="USD", callback_data=f"show_{coin_id}_usd")],
            [InlineKeyboardButton(text="RUB", callback_data=f"show_{coin_id}_rub")],
        ]
    )
    await callback.message.answer("Выбери валюту:", reply_markup=keyboard)
    await callback.answer()


@dp.callback_query(F.data.startswith("show_"))
async def show_callback(callback: CallbackQuery):
    coin_id = callback.data.split("_")[1]
    vs_currency = callback.data.split("_")[2]

    price = get_price(coin_id, vs_currency)

    if price is None:
        await callback.message.answer("Не удалось получить курс. Попробуй позже.")
    else:
        await callback.message.answer(
            f"{coin_id.capitalize()}: {price} {vs_currency.upper()}"
        )

    await callback.answer()


@dp.message(Command("add"))
async def add_handler(message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Укажи монету: /add bitcoin")
        return

    coin = parts[1].lower()
    add_favorite(message.from_user.id, coin)
    await message.answer(f"Монета {coin} добавлена в избранное.")


@dp.message(Command("remove"))
async def remove_handler(message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Укажи монету: /remove bitcoin")
        return

    coin = parts[1].lower()
    remove_favorite(message.from_user.id, coin)
    await message.answer(f"Монета {coin} удалена из избранного.")


@dp.message(Command("my"))
async def my_handler(message: Message):
    coins = get_favorites(message.from_user.id)

    if not coins:
        await message.answer("У тебя пока нет избранных монет. Добавь: /add bitcoin")
        return

    lines = []
    for coin in coins:
        price = get_price(coin, "usd")
        if price is None:
            lines.append(f"{coin.capitalize()}: не удалось получить курс")
        else:
            lines.append(f"{coin.capitalize()}: {price} USD")

    await message.answer("\n".join(lines))


@dp.message()
async def echo_handler(message: Message):
    await message.answer(f"Ты написал: {message.text}")


async def main():
    async def main():
        init_db()
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
