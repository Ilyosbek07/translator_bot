from aiogram import types
from googletrans import Translator
from loader import db, dp


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    try:
        await db.add_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
            type=1
        )
        await db.update_users_from_lang(from_lang='uz', to_lang='ru', tg_id=message.from_user.id)

    except Exception as err:
        pass

    try:
        langs = await db.get_from(tg_id=message.from_user.id)
        from_lang = ''
        to_lang = ''
        for i in langs:
            from_lang += f"{i[0]}"
            to_lang += f"{i[1]}"
        tar = Translator()
        a = tar.translate(f'{message.text}', src=f'{from_lang}', dest=f'{to_lang}').text
        await message.answer(text=a)
    except:
        await message.answer('Kechirasiz faqat 500 tagacha bo`lgan so`zlarni qabul qilamiz\n\n'
                             'Iltomos 500 tadan ortig`ini alohida kiriting')
