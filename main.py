from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from text_file import help_commands, hello_message
from parser import dictionary, urls, authors
from pprint import pprint
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = '***'
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

repkb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton(text='/start'))
repkb.add(KeyboardButton(text='/newbooks'))
repkb.add(KeyboardButton(text='/help'))



urlkb1 = InlineKeyboardMarkup(row_width=2)
for k in range(1, 7):
    button = InlineKeyboardButton(
        text=f'{dictionary[k]["Автор книги"]},\n {dictionary[k]["Название книги"]},\n {dictionary[k]["Читает"]}',
        url=urls[k])
    button2 = InlineKeyboardButton(
        text=f'{dictionary[k + 1]["Автор книги"]},\n {dictionary[k + 1]["Название книги"]},\n {dictionary[k + 1]["Читает"]}',
        url=urls[k + 1])
    button3 = InlineKeyboardButton(
        text=f'{dictionary[k + 2]["Автор книги"]},\n {dictionary[k + 2]["Название книги"]},\n {dictionary[k + 2]["Читает"]}',
        url=urls[k + 2])
    button4 = InlineKeyboardButton(
        text=f'{dictionary[k + 3]["Автор книги"]},\n {dictionary[k + 3]["Название книги"]},\n {dictionary[k + 3]["Читает"]}',
        url=urls[k + 3])
    button5 = InlineKeyboardButton(
        text=f'{dictionary[k + 4]["Автор книги"]},\n {dictionary[k + 4]["Название книги"]},\n {dictionary[k + 4]["Читает"]}',
        url=urls[k + 4])
    urlkb1.add(button, button2, button3, button4, button5)




@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(hello_message,
                         reply_markup=repkb,
                         parse_mode='HTML')


@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    await message.answer(help_commands,
                         reply_markup=repkb,
                         parse_mode="HTML")



@dp.message_handler(commands=['favour'], state=FSMContext)
async def favour(message: types.Message):
    await message.answer('Хорошо. Следующим сообщением назовите вашего любимого автора.')
    await State.set_state(answers.waiting_for_favour)



@dp.message_handler(commands=['newbooks'])
async def books(message: types.Message):
    await message.answer('Любите почитать? Это хорошо. Вот новые книги, которые появились за сегодня.',
                         reply_markup=urlkb1)



if __name__ == '__main__':
    logging.info("Starting bot...")
    executor.start_polling(dp)
