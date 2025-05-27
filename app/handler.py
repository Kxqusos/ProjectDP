import telebot
from telebot import types
import os
from dotenv import load_dotenv
load_dotenv()
from app.gpt_api import generate_recipe
from app.recognition import recognize_ingridients
from app.db import save_message
from app.config import TELEGRAM_TOKEN
import asyncio

bot = telebot.TeleBot(TELEGRAM_TOKEN)

MENU_BUTTONS = [
    "Отправить продукты текстом",
    "Распознать продукты с фото",
    "История запросов"
]

def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(btn) for btn in MENU_BUTTONS])
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Выбери, как хочешь ввести продукты:",
        reply_markup=main_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == "Отправить продукты текстом")
def menu_text(message):
    bot.send_message(message.chat.id, "Введите список ингредиентов через запятую:")

@bot.message_handler(func=lambda m: m.text == "Распознать продукты с фото")
def menu_photo(message):
    bot.send_message(message.chat.id, "Отправь фотографию с продуктами, которые хочешь распознать")

@bot.message_handler(func=lambda m: m.text == "История запросов")
def menu_history(message):
    bot.send_message(message.chat.id, "Функция еще не реализована")

@bot.message_handler(func=lambda m: m.text and m.text not in MENU_BUTTONS)
def handle_text(message):
    print("User ingredients:", message.text)
    ingredients = [x.strip() for x in message.text.split(",") if x.strip()]
    if not ingredients:
        bot.reply_to(message, "Пожалуйста, отправьте корректный список ингредиентов")
        return
    recipe = generate_recipe(ingredients)
    bot.reply_to(message, recipe)
    asyncio.create_task(save_message(message.from_user.id, message.from_user.username, message.text, recipe, 0))

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded = bot.download_file(file_info.file_path)
    img_path = f"photo_{message.chat.id}_{message.message_id}.jpg"
    with open(img_path, "wb") as f:
        f.write(downloaded)
        print("DEBUG: Сохранили файл", img_path, "размер:", os.path.getsize(img_path))
    ingredients = recognize_ingridients(img_path)
    if not ingredients:
        bot.reply_to(message, "Не удалось распознать продукты на фото")
        recipe = "fail"
    else:
        recipe = generate_recipe(ingredients)
        bot.reply_to(message, f"Распознал: {', '.join(ingredients)}\n\n{recipe}")
    asyncio.create_task(save_message(
        message.from_user.id,
        message.from_user.username,
        "PHOTO",
        recipe,
        1
    ))
    os.remove(img_path)