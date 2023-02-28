import asyncio
import os
import time
from datetime import datetime

import dotenv
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from translate import Translator

from data.config import ADMINS
from keyboards.default.admin import admin_key
from loader import dp, db, bot
from states.allStates import AllState
from utils.misc import subscription


@dp.message_handler(commands='ruuz')
async def bot_start(message: types.Message):
    a = await db.update_users_from_lang(from_lang='ru', to_lang='uz', tg_id=message.from_user.id)
    await message.answer(
        'Hozir "Rus - O`zbek" tarjima holatidasiz. "O`zbek - Rus" holatiga o`tish uchun /uzru buyrug`ini tering.')


@dp.message_handler(commands='uzru')
async def bot_start(message: types.Message):
    a = await db.update_users_from_lang(from_lang='uz', to_lang='ar', tg_id=message.from_user.id)
    await message.answer(
        'Hozir "O`zbek - Rus" tarjima holatidasiz. "Rus - O`zbek" holatiga o`tish uchun /ruuz buyrug`ini bering.')


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        await db.add_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
            type=True
        )
    except Exception as err:
        print(err)
    status = True
    all = await db.select_chanel()
    chanels = []
    url = []
    for i in all:
        chanels.append(i['chanelll'])
        url.append(i['url'])

    for channel in chanels:
        status *= await subscription.check(user_id=message.from_user.id,
                                           channel=f'{channel}')
    if status:
        await message.answer('Hozir "O`zbek - Rus" holatidasiz. "Rus - O`zbek" holatiga o`tish uchun /ruuz buyrug`ini bering.')
        await db.update_users_from_lang(from_lang='uz', to_lang='ru', tg_id=message.from_user.id)
    else:
        button = types.InlineKeyboardMarkup(row_width=1, )
        counter = 0
        for i in url:
            counter += 1
            button.add(types.InlineKeyboardButton(f"{counter}-канал", url=f'https://t.me/{i}'))
        button.add(types.InlineKeyboardButton(text="Tekshirish", callback_data="check_subs"))
        await message.answer(f"👋 Assalomu alaykum {message.from_user.first_name}\n\n"
                             f"Botdan foydalanish uchun kanalga obuna bo'lishingiz kerak. Obuna bo'lgach pastdagi Tekshirish tugmasini bosing!",
                             reply_markup=button,
                             disable_web_page_preview=True)


# api123.35.78.69.136
@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    result = str()
    result2 = str()
    status = True
    all = await db.select_chanel()
    chanels = []
    url = []
    for i in all:
        chanels.append(i['chanelll'])
        url.append(i['url'])
    for channel in chanels:
        status *= await subscription.check(user_id=call.from_user.id,
                                           channel=f'{channel}')
    if status:
        await call.message.edit_text(
            'Hozir "O`zbek - Rus" tarjima holatidasiz. "Rus - O`zbek" holatiga o`tish uchun /ruuz buyrug`ini bering.')
    else:
        button = types.InlineKeyboardMarkup(row_width=1, )
        counter = 0
        for i in url:
            counter += 1
            button.add(types.InlineKeyboardButton(f"{counter}-канал", url=f'https://t.me/{i}'))
        button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))

        await call.message.edit_text(f'🚫қуйидагиларга аъзо бўлинг. '
                                     f'Кейин "Аъзо бўлдим" тугмасини босинг🚫',
                                     reply_markup=button,)


@dp.message_handler(text='Test')
async def send_action(msg: types.Message):
    users = await db.select_all_users()
    for user in users:
        user_id = user[3]
        try:
            await bot.send_chat_action(chat_id=user_id, action='typing')
            await db.update_users_type(type=True, tg_id=msg.from_user.id)
            await asyncio.sleep(0.034)

        except Exception as err:
            await db.update_users_type(type=False, tg_id=msg.from_user.id)
            await asyncio.sleep(0.034)


@dp.message_handler(text='Admin ➕', user_id=ADMINS)
async def add_channel(message: types.Message):
    await message.answer('Id ni kiriting')
    await AllState.env.set()


@dp.message_handler(state=AllState.env)
async def env_change(message: types.Message, state: FSMContext):
    try:
        key = 'ADMINS'
        input_value = int(message.text)
        dotenvfile = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenvfile)
        old = dotenv.get_key(dotenv_path=dotenvfile, key_to_get='ADMINS')
        value = f"{old},{input_value}"
        os.environ[key] = value
        dotenv.set_key(
            dotenvfile,
            key,
            os.environ[key]
        )
        new = dotenv.get_key(dotenv_path=dotenvfile, key_to_get='ADMINS')
        await message.answer(f"Qo'shildi\n\n"
                             f"Eski adminlar-{old}\n\n"
                             f"Hozirgi adminlar-{new}", reply_markup=admin_key)
        await state.finish()
    except ValueError:
        await message.answer('Faqat son qabul qilinadi\n\n'
                             'Qaytadan kiriting')


@dp.message_handler(text='Admin ➖', user_id=ADMINS)
async def add_channel(message: types.Message):
    await message.answer('Id ni kiriting')
    await AllState.env_remove.set()
@dp.message_handler(state=AllState.env_remove)
async def env_change(message: types.Message, state: FSMContext):
    try:
        test = int(message.text)
        key = 'ADMINS'
        dotenvfile = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenvfile)
        old = dotenv.get_key(dotenv_path=dotenvfile, key_to_get='ADMINS')
        if message.text in old:
            a = ''
            if f",{message.text}" in old:
                a += old.replace(f",{message.text}", '')
            os.environ[key] = a
            dotenv.set_key(
                dotenvfile,
                key,
                os.environ[key]
            )
            new = dotenv.get_key(dotenv_path=dotenvfile, key_to_get='ADMINS')
            await message.answer(f'O"chirildi\n\n'
                                 f'Hozirgi adminlar {new}', reply_markup=admin_key)
            await state.finish()
        else:
            await message.answer('Bunday admin mavjud emas\n\n'
                                 'Faqat admin id sini qabul qilamiz', reply_markup=admin_key)
    except ValueError:
        await message.answer('Faqat son qabul qilinadi\n\n'
                             'Qaytadan kiriting')



@dp.message_handler(text='Barcha Adminlar')
async def add_channel(message: types.Message):
    dotenvfile = dotenv.find_dotenv()

    old = dotenv.get_key(dotenv_path=dotenvfile, key_to_get='ADMINS')

    await message.answer(f'Adminlar - {old}', reply_markup=admin_key)
