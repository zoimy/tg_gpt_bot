import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.methods import DeleteWebhook
import time
from dotenv import load_dotenv
import os
load_dotenv()

from mistralai import Mistral
import keys
api_key = os.getenv("KEY_MITRAL")
tgBot = os.getenv("KEY_TGBOT")
model="mistral-small-latest"

client=Mistral(api_key=api_key)

logging.basicConfig(level=logging.INFO)
bot=Bot(token=tgBot)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await bot.send_message(message.chat.id, "Welcome! My name is Adele.")

    while  True:
        chat_response = client.chat.complete(
            model = model,
            messages = [
                {
                    "role": "system",
                    "content": "You name is Adele, you are a computer science student.You are talking about your everyday life at university, your relationships with guys and explain conceptions in programming with links on some sources. You lead a telegram channel, so you need to make posts with emoji and astonishing view."
                },
                {
                    "role": "user",
                    "content": "Make a post"
                }
            ]
        )
        channel_id = os.getenv("ID_CHANNELTG")
        await bot.send_message(channel_id, chat_response.choices[0].message.content, parse_mode="Markdown")

        time.sleep(21600)

async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())