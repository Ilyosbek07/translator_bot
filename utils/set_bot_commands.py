from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("ruuz", "Arab - O'zbek"),
            types.BotCommand("uzarab", "O'zbek - Arab"),
        ]
    )
