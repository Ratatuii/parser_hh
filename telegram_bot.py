import asyncio
import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from os import getenv
from main import check_update_vacancy
from aiogram.utils.markdown import hlink, hbold, hunderline

chat_id = 352591777
API_TOKEN = getenv("API_TOKEN")
if not API_TOKEN:
    exit("Error: no token provided")
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['All vacancy', 'Last 5 vacancy', 'Fresh vacancy']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    print(message.chat.id)
    await message.answer('Hello i`m telegram bot with actually vacancy python developer', reply_markup=keyboard)

# 352591777

@dp.message_handler(Text('All vacancy'))
async def get_all_vacancy(message: types.Message):
    check_update_vacancy()
    with open('result.json') as file:
        result = json.load(file)
    for key, value in list(result.items())[:-11:-1]:
        vacancy = f'{hlink(value["Title"], value["Url"])}'
        await message.answer(vacancy)
        await asyncio.sleep(0.4)


@dp.message_handler(Text('Last 5 vacancy'))
async def get_last_five_vacancy(message: types.Message):
    check_update_vacancy()
    with open('result.json') as file:
        result = json.load(file)
    for key, value in list(result.items())[:-6:-1]:
        vacancy = f'{hlink(value["Title"], value["Url"])}'
        await message.answer(vacancy)
        await asyncio.sleep(0.4)


@dp.message_handler(Text('Fresh vacancy'))
async def get_fresh_vacancy(message: types.Message):

    new_vacancy = check_update_vacancy()

    if len(list(new_vacancy)) >= 1:
        for key, value in list(new_vacancy.items())[::-1]:
            vacancy = f'{hlink(value["Title"], value["Url"])}'
            await message.answer(vacancy)
            await asyncio.sleep(0.4)
    else:
        await message.answer('There is no fresh news yet...')


async def vacancy_every_ten_minutes():
    while True:
        new_vacancy = check_update_vacancy()

        if len(new_vacancy) >= 1:
            for key, value in list(new_vacancy.items())[::-1]:
                vacancy = f'{hlink(value["Title"], value["Url"])}'
                await bot.send_message(chat_id, vacancy, disable_notification=True)
        else:
            await bot.send_message(chat_id, 'There is no fresh news yet...', disable_notification=True)
        await asyncio.sleep(120)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(vacancy_every_ten_minutes())
    executor.start_polling(dp)

