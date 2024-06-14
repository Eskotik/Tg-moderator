import json
import logging
import time
import datetime
import asyncio
import re
from aiogram import executor, types, Bot, Dispatcher, types
from aiogram.dispatcher.filters import AdminFilter, IsReplyFilter
from random import randint
from millify import millify
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    logging.basicConfig(level=logging.INFO)


adminId = os.getenv("ADMIN_ID")
token1 = os.getenv("BOT_TOKEN")

exemptChannelId = os.getenv("EXEMPT_CHANNEL_ID")
whiteChannelId = os.getenv("WHITE_CHANNEL_ID")

bot = Bot(token=token1, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
CoinMarketCapKey = os.getenv("COINMARKETCAP_KEY")

# with open("tickers.json") as f:
#     COIN_TICKERS = json.load(f)


# def get_coin_price(coin_ticker):
#     coin_id = COIN_TICKERS.get(coin_ticker.lower())
#     if not coin_id:
#         return f"Не удалось найти данные о {coin_ticker}"

#     url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
#         if coin_id in data:
#             coin_data = data[coin_id]
#             price = coin_data["usd"]
#             market_cap = coin_data.get("usd_market_cap", 0)
#             volume_24h = coin_data.get("usd_24h_vol", 0)
#             market_cap_formatted = millify(market_cap, precision=2)
#             volume_24h_formatted = millify(volume_24h, precision=2)
#             if price > 1:
#                 price_formatted = f"{price:.2f}"
#             elif price > 0.01 and price < 1:
#                 price_formatted = f"{price:.5f}"
#             else:
#                 price_formatted = f"{price:.9f}"
#             return (
#                 f"Цена {coin_ticker.upper()}: ${price_formatted}\n"
#                 f"Рыночная капитализация: ${market_cap_formatted}\n"
#                 f"24ч Объем: ${volume_24h_formatted}"
#             )
#         else:
#             return f"Не удалось найти данные о {coin_ticker}"
#     except requests.RequestException as e:
#         return f"Ошибка запроса API: {e}"

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


def get_coin_price(coin_symbol):
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    parameters = {"symbol": coin_symbol.upper()}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "f97a825f-6f87-4d4c-8e9e-56af3743dd19",
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        if "data" in data and coin_symbol.upper() in data["data"]:
            coin_data = data["data"][coin_symbol.upper()][0]
            name = coin_data["name"]
            price = coin_data["quote"]["USD"]["price"]
            percent_24h = coin_data["quote"]["USD"]["percent_change_24h"]
            volume_24h = coin_data["quote"]["USD"]["volume_24h"]
            market_cap = coin_data["quote"]["USD"]["market_cap"]
            percent_24h_formatted = f"{percent_24h:.2f}"
            market_cap_formatted = millify(market_cap, precision=2)
            volume_24h_formatted = millify(volume_24h, precision=2)
            if price > 1:
                price_formatted = f"{price:.2f}"
            elif price > 0.01 and price < 1:
                price_formatted = f"{price:.5f}"
            else:
                price_formatted = f"{price:.9f}"
                # if percent24h have a +, add a "+"
            return (
                f"{name} ({coin_symbol.upper()}):"
                f" ${price_formatted}\n"
                f"Изменение цены за 24ч: {percent_24h_formatted}%\n"
                f"Объем торгов за 24ч: ${volume_24h_formatted}\n"
                f"Рыночная капитализация: ${market_cap_formatted}"
            )
        else:
            return f"Не удалось найти информацию о монете {coin_symbol.upper()}"

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return f"Ошибка при получении данных: {e}"
    except KeyError:
        return f"Ошибка: Неожиданная структура данных в ответе API для {coin_symbol.upper()}"


@dp.message_handler(commands=["p"])
async def get_price(message: types.Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply(
            "Пожалуйста, укажите символ монеты после команды /p\nНапример: /p BTC"
        )
        return

    coin_symbol = parts[1].upper()

    try:
        result = get_coin_price(coin_symbol)
        await message.reply(result)
    except Exception as e:
        logging.error(f"Ошибка при получении данных для {coin_symbol}: {e}")
        await message.reply(
            f"Произошла ошибка при получении данных для {coin_symbol}. Пожалуйста, попробуйте позже или проверьте правильность символа монеты."
        )


@dp.message_handler(commands=["p"])
async def get_price(message: types.Message):
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply(
            "Пожалуйста, укажите символ монеты после команды /p\nНапример: /p BTC"
        )
        return

    coin_symbol = parts[1].upper()

    try:
        result = get_coin_price(coin_symbol)
        await message.reply(result)
    except Exception as e:
        logging.error(f"Ошибка при получении цены для {coin_symbol}: {e}")
        await message.reply(
            f"Произошла ошибка при получении данных для {coin_symbol}. Пожалуйста, попробуйте позже или проверьте правильность символа монеты."
        )


@dp.message_handler(content_types=["new_chat_members"])
async def new_chat_member(message: types.Message):
    chat_id = message.chat.id
    user = message.new_chat_members[0]
    user_name = user.first_name
    user_id = user.id
    user_mention = f"[{user_name}](tg://user?id={user_id})"

    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    welcome_message = await bot.send_message(
        chat_id=chat_id,
        text=f"Я видел тебя во сне, {user_mention}. Оракул предсказала твоё прибытие. Добро пожаловать в Матрицу Правды.",
        parse_mode=types.ParseMode.MARKDOWN,
    )

    asyncio.create_task(
        delete_message_after_delay(
            welcome_message.chat.id, welcome_message.message_id, 20
        )
    )


@dp.message_handler(content_types=["left_chat_member"])
async def leave_chat(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.message_handler(
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=["me"]
)
async def welcome(message: types.Message):
    if message.from_user.username is None:
        await message.reply(
            f"Name - {message.from_user.full_name}\nID - {message.from_user.id}\n"
        )
    else:
        await message.reply(
            f"Name - {message.from_user.full_name}\n"
            f"ID - <code>{message.from_user.id}</code>\n"
            f"Псевдоним - @{message.from_user.username}\n"
        )


@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    commands=["ban"],
    commands_prefix="!",
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
)
async def ban(message: types.Message):
    replied_user = message.reply_to_message.from_user.id
    admin_id = message.from_user.id
    await bot.kick_chat_member(chat_id=message.chat.id, user_id=replied_user)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"[{message.reply_to_message.from_user.full_name}]"
        f"(tg://user?id={replied_user})"
        f" был забанен админом [{message.from_user.full_name}]"
        f"(tg://user?id={admin_id})",
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    commands=["unban"],
    commands_prefix="!",
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
)
async def unban(message: types.Message):
    replied_user = message.reply_to_message.from_user.id
    await bot.unban_chat_member(chat_id=message.chat.id, user_id=replied_user)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"[{message.reply_to_message.from_user.full_name}](tg://user?id={replied_user}) был разбанен в чате.",
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    commands=["mute"],
    commands_prefix="!",
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
)
async def mute(message: types.Message):
    args = message.text.split()

    if len(args) > 1:
        till_date = args[1]
    else:
        till_date = "15m"

    if till_date[-1] == "m":
        ban_for = int(till_date[:-1]) * 60
    elif till_date[-1] == "h":
        ban_for = int(till_date[:-1]) * 3600
    elif till_date[-1] == "d":
        ban_for = int(till_date[:-1]) * 86400
    else:
        ban_for = 15 * 60

    replied_user = message.reply_to_message.from_user.id
    now_time = int(time.time())

    try:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=replied_user,
            permissions=types.ChatPermissions(can_send_messages=False),
            until_date=now_time + ban_for,
        )
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"[{message.reply_to_message.from_user.full_name}](tg://user?id={replied_user}) был заглушен на {till_date}",
            parse_mode=types.ParseMode.MARKDOWN,
        )
    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id, text=f"Не удалось заглушить: {str(e)}"
        )


@dp.message_handler(
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=["dont_click_me"],
)
async def mute_random(message: types.Message):
    now_time = int(time.time())
    replied_user_id = message.from_user.id
    replied_user = message.from_user.full_name
    random_m = randint(1, 10)
    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=replied_user_id,
        permissions=types.ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_other_messages=False,
        ),
        until_date=now_time + 60 * random_m,
    )
    await bot.send_message(
        text=f"[{replied_user}](tg://user?id={replied_user_id})"
        f" выиграл(а) мут на {random_m} минут(ы)",
        chat_id=message.chat.id,
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    commands_prefix="!",
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=["unmute"],
)
async def un_mute_user(message: types.Message):
    replied_user = message.reply_to_message.from_user.id
    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=replied_user,
        permissions=types.ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
        ),
    )
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(
        text=f"[{message.reply_to_message.from_user.full_name}](tg://user?id={replied_user})"
        f" можешь писать в чат )",
        chat_id=message.chat.id,
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=["pin"],
    commands_prefix="!",
)
async def pin_message(message: types.Message):
    msg_id = message.reply_to_message.message_id
    await bot.pin_chat_message(message_id=msg_id, chat_id=message.chat.id)


@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    commands_prefix="!",
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=["unpin"],
)
async def unpin_message(message: types.Message):
    msg_id = message.reply_to_message.message_id
    await bot.unpin_chat_message(message_id=msg_id, chat_id=message.chat.id)


@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    commands_prefix="!",
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=["del"],
)
async def delete_message(message: types.Message):
    msg_id = message.reply_to_message.message_id
    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.message_handler(
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=["report"]
)
async def report_by_user(message: types.Message):
    msg_id = message.reply_to_message.message_id
    user_id = message.from_user.id
    admins_list = await message.chat.get_administrators()

    for admin in admins_list:
        try:
            await bot.send_message(
                text=f"User: [{message.from_user.full_name}](tg://user?id={user_id})\n"
                f"Репорт за следующее сообщение:\n"
                f"[Возможное нарушение](t.me/{message.chat.username}/{msg_id})",
                chat_id=admin.user.id,
                parse_mode=types.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )
        except Exception as e:
            logging.debug(
                f"\nCan't send report message to {admin.user.id}\nError - {e}"
            )

    await message.reply("Было отправлено админам!")


warnings = {}


async def delete_message_after_delay(chat_id, message_id, delay):
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print(f"не удалось удалить сообщение: {e}")


def load_forbidden_words():
    with open("forbidden_words.json", "r", encoding="utf-8") as file:
        return json.load(file)


forbidden_words = load_forbidden_words()


def contains_forbidden_word(message_text):
    text_words = set(re.split(r"\W+", message_text.lower()))
    for phrase in forbidden_words:
        phrase_words = set(re.split(r"\W+", phrase.lower()))
        if phrase_words.issubset(text_words) or re.search(
            rf"{phrase}[?!,.@#*&^:;()$]?", message_text, re.IGNORECASE
        ):
            return True
    return False


@dp.message_handler(content_types=["text", "reply_to_message", "photo", "video"])
async def handle_text_messages(message: types.Message):
    if message.sender_chat and str(message.sender_chat.id) == exemptChannelId:
        return

    if (
        message.forward_from_chat
        and str(message.forward_from_chat.id) == exemptChannelId
    ):
        return

    is_admin = await AdminFilter(is_chat_admin=True).check(message)
    user_id = message.from_user.id
    username = (
        message.from_user.username
        if message.from_user.username
        else message.from_user.first_name
    )

    print(message)

    if not is_admin:

        if "forward_from_chat" in message:
            if str(message.forward_from_chat.id) != whiteChannelId:
                await handle_violation(
                    message,
                    message.from_user.username,
                    message.from_user.id,
                    "пересылку сообщений из других каналов",
                )

        if message.forward_from:
            await handle_violation(
                message,
                message.from_user.username,
                message.from_user.id,
                "пересылку сообщений из других ботов",
            )

        if message.text and contains_forbidden_word(message.text):
            await handle_violation(
                message, username, user_id, "запрещенные слова и фразы"
            )

        if message.caption and contains_forbidden_word(message.caption):
            await handle_violation(
                message, username, user_id, "запрещенные слова и фразы"
            )
            return
        # Trading View unlock
        for entity in message.entities:
            if entity.type == "url":
                url = message.text[entity.offset : entity.offset + entity.length]
                if not url.startswith("https://www.tradingview.com/"):
                    await handle_violation(message, username, user_id, "ссылки")
                    break  # This break statement should be inside the if block


async def handle_violation(message, username, user_id, violation_type):
    if user_id not in warnings:
        warnings[user_id] = 1
        warning_message = await message.reply(
            f"@{username}, <b><u>Я не могу позволить еще хоть одному человеку быть обманутым Матрицей🕶</u></b>. Предупреждение [{warnings[user_id]} c 3] за {violation_type}.",
            parse_mode="HTML",
        )
    else:
        warnings[user_id] += 1
        if warnings[user_id] <= 3:
            warning_message = await message.reply(
                f"@{username}, <b><u>Я не могу позволить еще хоть одному человеку быть обманутым Матрицей🕶</u></b>. Предупреждение [{warnings[user_id]} c 3] за {violation_type}.",
                parse_mode="HTML",
            )
        else:
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                until_date=datetime.datetime.now() + datetime.timedelta(minutes=1),
                can_send_messages=False,
            )
            await message.reply(
                f"@{username}, вы были заглушены на 5 часов за {violation_type}."
            )
            await bot.delete_message(message.chat.id, message.message_id)

            warnings[user_id] = 0

    asyncio.create_task(
        delete_message_after_delay(
            warning_message.chat.id, warning_message.message_id, 10
        )
    )
    await bot.delete_message(message.chat.id, message.message_id)


executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
