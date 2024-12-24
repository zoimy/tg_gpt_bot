import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.methods import DeleteWebhook
import time

from mistralai import Mistral
import keys
api_key = keys.key_mitral
model="mistral-small-latest"

client=Mistral(api_key=api_key)

logging.basicConfig(level=logging.INFO)
bot=Bot(token=keys.key_tgBot)
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
        channel_id = keys.id_channelTg
        await bot.send_message(channel_id, chat_response.choices[0].message.content, parse_mode="Markdown")

        time.sleep(21600)

async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())