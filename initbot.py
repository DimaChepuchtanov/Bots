from telebot.async_telebot import AsyncTeleBot
import configparser

"""
Иницилизация бота
"""

config = configparser.ConfigParser()
config.read("setting.conf")
work_bot = AsyncTeleBot(token=config['Setting bot']['token'],
                        colorful_logs=True)
