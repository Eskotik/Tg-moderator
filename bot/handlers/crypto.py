import logging

from aiogram import types

from bot.loader import dp
from bot.services.crypto import get_coin_price


@dp.message_handler(commands=["p"])
async def get_price(message: types.Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply(
            "Please specify the coin symbol after the /p command\nExample: /p BTC"
        )
        return

    coin_symbol = parts[1].upper()

    try:
        result = get_coin_price(coin_symbol)
        await message.reply(result)
    except Exception as e:
        logging.error("Error retrieving data for %s: %s", coin_symbol, e)
        await message.reply(
            f"An error occurred while retrieving data for {coin_symbol}. "
            "Please try again later or check the coin symbol."
        )
