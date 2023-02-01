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
        '"Rus - O`zbek" holatiga o`tildi. "O`zbek - Rus" holatiga o`tish uchun /uzru buyrug`ini bering.')


@dp.message_handler(commands='uzru')
async def bot_start(message: types.Message):
    a = await db.update_users_from_lang(from_lang='uz', to_lang='ru', tg_id=message.from_user.id)
    await message.answer(
        '"O`zbek - Rus" holatiga o`tildi. "Rus - O`zbek" holatiga o`tish uchun /ruuz buyrug`ini bering.')


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
        await db.update_users_from_lang(from_lang='ru', to_lang='uz', tg_id=message.from_user.id)
        await message.answer(
            '"Rus - O`zbek" holatiga o`tildi. "O`zbek - Rus" holatiga o`tish uchun /uzru buyrug`ini bering.')
    else:
        button = types.InlineKeyboardMarkup(row_width=1, )
        counter = 0
        for i in url:
            counter += 1
            button.add(types.InlineKeyboardButton(f"{counter}-канал", url=f'https://t.me/{i}'))
        button.add(types.InlineKeyboardButton(text="Tekshirish", callback_data="check_subs"))
        await message.answer(f"👋 Assalomu alaykum {message.from_user.first_name}\n\n"
                             f"Botdan foydalanish uchun @cchannel kanaliga obuna bo'lishingiz kerak. Obuna bo'lgach pastdagi Tekshirish tugmasini bosing!",
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
            '"Rus - O`zbek" holatiga o`tildi. "O`zbek - Rus" holatiga o`tish uchun /uzru buyrug`ini bering.')
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


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    try:
        langs = await db.get_from(tg_id=message.from_user.id)
        from_lang = ''
        to_lang = ''
        for i in langs:
            from_lang += f"{i[0]}"
            to_lang += f"{i[1]}"

        translator = Translator(from_lang=f'{from_lang}', to_lang=f"{to_lang}")
        text = message.text
        a = translator.translate(f"{text}")
        await message.answer(text=a, disable_notification=True)
    except:
        await message.answer('Kechirasiz faqat 500 tagacha bo`lgan so`zlarni qabul qilamiz\n\n'
                             'Iltomos 500 tadan ortig`ini alohida kiriting')
