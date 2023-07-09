from initbot import work_bot
import asyncio

"""
Бот асинхроно проверяет пользователей на вход и исключает их, если их нет в списке
"""

@work_bot.message_handler(commands=['start'])
async def echo_message(message):
    await work_bot.reply_to(message, message.text)


if __name__ == "__main__":
    asyncio.run(work_bot.polling())
