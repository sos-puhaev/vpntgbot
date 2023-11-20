from loader import bot
import asyncio
from aiogram import executor
from handlers import dp

async def on_shutdown(dp):
    await bot.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=on_shutdown, skip_updates=True)