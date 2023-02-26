from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from translate import Translator

from loader import dp, db
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
            full_name=message.from_user.full_name
        )
    except:
        pass
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
                                     reply_markup=button,
                                     disable_web_page_preview=True)
