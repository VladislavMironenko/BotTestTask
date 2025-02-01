from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from postgres import take_deal_id , create_table , create_record
from openai_gpt import sync_generate_text
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import os
from bitrix import create_deal , update_deal


executor = ThreadPoolExecutor()
load_dotenv()
is_gpt_dialog_active = {}
is_questions_active_company = {}
is_questions_active_private_person = {}
result_questions = {}
user_answers = {}
user_questions = {}
user_questions_text = {}

bot = Bot(token=os.getenv('TG_TOKEN'))
dp = Dispatcher()

# create_table()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    is_gpt_dialog_active[message.from_user.id] = False
    kb = [
        [KeyboardButton(text="Компания"), KeyboardButton(text="Частное лицо")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer("Приветствую!" ,reply_markup=keyboard)

@dp.message(F.text.lower() == "компания")
async def start_questions_for_company(message: types.Message):
    user_id = message.from_user.id
    is_gpt_dialog_active[message.from_user.id] = False
    is_questions_active_company[message.from_user.id] = True
    is_questions_active_private_person[message.from_user.id] = False
    user_answers[user_id] = []
    user_questions_text[user_id] = []

    with open('./questions_company.txt', 'r' , encoding='utf-8') as e:
        questions = [line.strip() for line in e.readlines() if line.strip()]
    if questions:
        user_questions_text[user_id].append(questions[0].strip())
        await message.reply(questions[0].strip())


@dp.message(F.text.lower() == "частное лицо")
async def start_questions_for_private_person(message: types.Message):
    user_id = message.from_user.id
    is_gpt_dialog_active[message.from_user.id] = False
    is_questions_active_company[message.from_user.id] = False
    is_questions_active_private_person[message.from_user.id] = True
    user_answers[user_id] = []
    user_questions_text[user_id] = []

    with open('./questions_private_person.txt', 'r' , encoding='utf-8') as e:
        questions = [line.strip() for line in e.readlines() if line.strip()]
    if questions:
        user_questions_text[user_id].append(questions[0].strip())
        await message.reply(questions[0].strip())

async def generate_text(user_name ,text):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, sync_generate_text, user_name,text)


@dp.message(F.text)
async def func_for_questions(message: types.Message):
    user_id = message.from_user.id

    if is_gpt_dialog_active[message.from_user.id] == True:
        kb = [
            [KeyboardButton(text="Задать дополнительный вопрос"), KeyboardButton(text="Связаться с менеджером") ,KeyboardButton(text="Перейти к оплате")]
        ]
        keyboard = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        take_deal_id_res = take_deal_id(user_id)
        response = await generate_text(message.from_user.username , message.text)
        update_deal(take_deal_id_res , f'User : {message.text}' , f'AI : {response}')

        await message.reply(response , reply_markup=keyboard)
    elif is_questions_active_company[message.from_user.id] == True or is_questions_active_private_person[message.from_user.id] == True:
        user_answers[user_id].append(message.text.strip())
        if is_questions_active_company[message.from_user.id] == True:
            segment = 'Компания'
            with open('./questions_company.txt', 'r' , encoding='utf-8') as e:
                questions = [line.strip() for line in e.readlines() if line.strip()]
        elif is_questions_active_private_person[message.from_user.id] == True:
            segment = 'Частное лицо'
            with open('./questions_private_person.txt', 'r' , encoding='utf-8') as e:
                questions = [line.strip() for line in e.readlines() if line.strip()]
        if user_id not in user_questions:
            user_questions[user_id] = 0
        user_questions[user_id] += 1

        if user_questions[user_id] < len(questions):
            user_questions_text[user_id].append(questions[user_questions[user_id]].strip())
            await message.reply(questions[user_questions[user_id]].strip())
        else:
            is_questions_active_company[user_id] = False
            is_questions_active_private_person[user_id] = False
            is_gpt_dialog_active[user_id] = True
            result_questions = []
            for i in range(user_questions[user_id]):
                result_questions.append(f'{user_questions_text[user_id][i]} - {user_answers[user_id][i]}')
            deal_id = create_deal(user_id, segment, result_questions)
            create_record(user_id , segment, result_questions , deal_id)
            del user_answers[user_id]
            del user_questions_text[user_id]
            del user_questions[user_id]
            await message.answer('Ты прошел опрос , если есть еще вопросы , я внимательно слушаю')

    else:
        await message.reply("Отменяю текущее диалог")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())