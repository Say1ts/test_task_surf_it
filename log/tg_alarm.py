import asyncio
from typing import Optional

from aiogram import Bot

token: Optional[str] = None
chat_id: Optional[int] = None


async def send_telegram_message(message: str):
    if token and chat_id and message:
        bot = Bot(token=token)
        await bot.send_message(chat_id, text=message)
    else:
        print('There is no token or chat_id for sending telegram message')


def alert_critical_error(message):
    loop = asyncio.get_event_loop()
    loop.create_task(send_telegram_message(message))
