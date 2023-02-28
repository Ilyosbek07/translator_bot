from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.admin import admin_key
from keyboards.default.admin import back
from loader import dp, db
from states.allStates import AllState


@dp.message_handler(commands=['admin'], user_id=ADMINS)
async def admin(message: types.Message):
    await message.answer(text='Admin panel',
                         reply_markup=admin_key)


@dp.message_handler(text='Kanal ➕', user_id=ADMINS)
async def add_channel(message: types.Message):
    await message.answer(text='Kanalni kiriting\n\n'
                              'Masalan : "@Chanel zayavkada bo`lsa chanel_id(-123123213),chanel_url"\n\n',
                         reply_markup=back)
    await AllState.add.set()


@dp.message_handler(state=AllState.add)
async def add_username(message: types.Message, state: FSMContext):
    text = message.text
    if text[0] == '@':
        await db.add_chanell(chanelll=f"{text}", url=f"{text[1:]}")
        await message.answer("Qo'shildi", reply_markup=admin_key)
        await state.finish()
    elif text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    elif text[0] == '-':
        split_chanel = message.text.split(',')
        chanel_lst = []
        url_lst = []
        for i in split_chanel:
            lst = i.split('and')
            chanel_lst.append(lst[0])
            url_lst.append(lst[1])
        chanel = f'{chanel_lst}'
        url = f'{url_lst}'
        ch_text = chanel.replace("'", '')
        ch_text2 = ch_text.replace(" ", '')
        u_text = url.replace("'", '')
        u_text2 = u_text.replace(" ", '')

        await db.add_chanell(chanelll=ch_text2[1:-1], url=u_text2[1:-1])
        await message.answer("Qo'shildi", reply_markup=admin_key)
        await state.finish()

    else:
        await message.answer('Xato\n\n'
                             '@ belgi bilan yoki kanal id(-11001835334270andLink) sini link bilan birga kiriting kiriting')


@dp.message_handler(text='Kanal ➖', user_id=ADMINS)
async def add_channel(message: types.Message):
    await message.answer(text='Kanalni kiriting @ belgi bilan\n\n'
                              'Masalan : "Kanal zayavkada bo`lsa chanel_id(-123123213),chanel_url"\n\n',
                         reply_markup=back)
    await AllState.delete.set()


@dp.message_handler(state=AllState.delete)
async def del_username(message: types.Message, state: FSMContext):
    txt = message.text
    if txt[0] == '-':
        chanel = await db.get_chanel(channel=txt)
        if not chanel:
            await message.answer("Kanal topilmadi\n"
                                 "Qaytadan urinib ko'ring")

        else:
            await db.delete_channel(chanel=txt)
            await message.answer('Kanal o"chirildi', reply_markup=admin_key)
            await state.finish()

        # await message.answer("O'chirildi")
        # await state.finish()
    elif txt[0] == '@':
        chanel = await db.get_chanel(channel=f"{txt}")
        if not chanel:
            await message.answer("Kanal topilmadi\n"
                                 "Qaytadan urinib ko'ring")

        else:
            await db.delete_channel(chanel=txt)
            await message.answer('Kanal o"chirildi', reply_markup=admin_key)
            await state.finish()
    elif txt == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()


@dp.message_handler(text='Statistika 📊')
async def show_users(message: types.Message):
    a = await db.count_users()
    active = await db.count_active_users()
    block = await db.count_block_users()
    await message.answer(f'<b>🔷 Jami obunachilar: {a} tа</b>\n\n'
                         f'Active: {active}\n'
                         f'Block: {block}')


@dp.message_handler(text='🏘 Bosh menu')
async def menuu(message: types.Message):
    await message.answer('Bosh menu', reply_markup=admin_key)


@dp.message_handler(text='Kanallar 📈')
async def channels(message: types.Message):
    channels = await db.select_chanel()
    text = ''
    for channel in channels:
        text += f"{channel['chanelll']}\n"
    try:
        await message.answer(f"{text}", reply_markup=admin_key)
    except:
        await message.answer(f"Kanallar mavjud emas")
