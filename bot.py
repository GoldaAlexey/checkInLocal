import time
import logging
import string

from aiogram import Bot, Dispatcher, executor, types
import players
from players import Player

players_list = []
TOKEN = "6164107153:AAHuB66sQ8EtxnnpOzSnC5c6MwYARS6799c"
ADMIN_ID = 202064123

list_of_commands = ['help', 'start', 'show_social_list', 'start']
bot = Bot(token = TOKEN)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands='start')
async def start_handler(message: types.Message):
    player = Player(first_name=message.from_user.first_name,
                    username=message.from_user.username,
                    account_id=message.from_user.id)
    print(message)
    kb = [
        [
            types.KeyboardButton(text="Узнать свои социальные кредиты"),
            types.KeyboardButton(text="Донести на нарушителя!")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Что вам интересно?"
    )
    if players.add_user(player=player):
        await message.answer(f"Привет, {player.first_name} теперь ты часть социального мира!\n", reply_markup=keyboard)
    else:
        await message.answer(f"Привет, {player.first_name} ты и так часть социального мира!", reply_markup=keyboard)

@dp.message_handler(commands='show_players')
async def test_handler(message: types.Message):
    player = players.get_list_of_players()
    answer_message = "Список игроков:\n\n" +\
                    ("\n".join(["username: "+p['first_name']+" social_credits: "+str(p['social_credits']) for p in player]))
    await message.answer(answer_message)

@dp.message_handler(commands='show_social_list')
async def show_social_list_handler(message: types.Message):
    if (message.from_user.id == ADMIN_ID):
        await message.reply(f"Привет, вот список всех гражданинов мира:")
        counter = 1
        for player in players_list:
            await message.reply(f"{counter}) {player.first_name}")
            counter = counter + 1

@dp.message_handler(commands='add')
async def add_handler(message: types.Message):
    print(message)
    parse_message = message.text.split()
    print(parse_message)
    await message.answer(f"В процессе разработки :)")

@dp.message_handler(commands='help')
async def help_handler(message: types.Message):
    await message.answer(f"В процессе разработки :)")

@dp.message_handler()
async def null_command_handler(message: types.Message):
    if message.text == None : 
        kb = [
            [
                types.KeyboardButton(text="Узнать свои социальные кредиты"),
                types.KeyboardButton(text="Донести на нарушителя!")
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Что вам интересно?"
        )
        await message.answer("Чего изволите?", reply_markup=keyboard)
    else :
        if message.text == "Узнать свои социальные кредиты" :
            user_social_credit = players.get_player_sc_by_account_id(message.from_user.id)
            if isinstance(user_social_credit, int) :
                await message.answer(f"Ваши социальные кредиты: {user_social_credit}")
            else :
                await message.answer("Ваши социальные кредиты: c ними что-то не так :0")
            kb = [
                [
                    types.KeyboardButton(text="Узнать свои социальные кредиты"),
                    types.KeyboardButton(text="Донести на нарушителя!")
                ],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
                input_field_placeholder="Что вам интересно?"
            )
            await message.answer("Чего еще изволите?", reply_markup=keyboard)
        elif message.text == "Донести на нарушителя!" :
                player = players.get_list_of_players()
                names = []
                kb = []
                for pl in player :
                    name = "нарушитель @"+"".join(pl['first_name'])
                    name = types.KeyboardButton(text="".join(name))
                    names += [name]
                kb = [names]
                keyboard = types.ReplyKeyboardMarkup(
                    keyboard=kb,
                    resize_keyboard=True,
                    input_field_placeholder="Что вам интересно?"
                )
                await message.answer("Кто из них нарушитель?!", reply_markup=keyboard)
        else :
            kb = [
                [
                    types.KeyboardButton(text="Узнать свои социальные кредиты"),
                    types.KeyboardButton(text="Донести на нарушителя!")
                ],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
                input_field_placeholder="Что вам интересно?"
            )
            await message.answer("Чего изволите?", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp)
