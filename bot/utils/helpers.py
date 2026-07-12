import asyncio
import logging
import time

from bot.loader import bot


async def delete_message_after_delay(chat_id: int, message_id: int, delay: int) -> None:
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logging.debug("Failed to delete message: %s", e)


def parse_mute_duration(till_date: str) -> int:
    if till_date[-1] == "m":
        return int(till_date[:-1]) * 60
    if till_date[-1] == "h":
        return int(till_date[:-1]) * 3600
    if till_date[-1] == "d":
        return int(till_date[:-1]) * 86400
    return 15 * 60
