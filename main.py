import logging

from aiogram import executor

from bot.handlers import register_handlers
from bot.loader import dp

register_handlers()


def main():
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
