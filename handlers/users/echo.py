from aiogram import types
from translate import Translator

from loader import db, dp


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
