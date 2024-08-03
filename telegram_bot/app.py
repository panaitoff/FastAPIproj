import os
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
API_URL = os.getenv("API_URL")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer("Welcome to the bot! Use /messages to see messages and /new to create a new message.")

@dp.message(Command('messages'))
async def get_messages(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/api/v1/messages/") as resp:
            messages = await resp.json()
            formatted_messages = "\n".join([msg['content'] for msg in messages])
            await message.answer(formatted_messages)

@dp.message(Command('new'))
async def new_message(message: types.Message):
    await message.answer("Please enter the new message content:")

@dp.message()
async def create_message(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/api/v1/message/", json={"content": message.text}) as resp:
            if resp.status == 200:
                await message.answer("Message created!")
            else:
                await message.answer("Failed to create message.")

if __name__ == '__main__':
    dp.run_polling(bot)