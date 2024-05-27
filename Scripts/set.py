from aiogram import Router
from aiogram import types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F

import json

s = Router()
choice = ['✅Yes', '🚫No']
keyboard = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="✅Yes"),
                                               types.KeyboardButton(text="🚫No")]], resize_keyboard=True)

class Speed(StatesGroup):
    speed = State()

class Noise(StatesGroup):
    ns = State()

class Mirror(StatesGroup):
    mr = State()

with open('jsons/settings.json', 'r') as file:
    data = json.load(file)

@s.message(Command('set'), StateFilter(None))
async def set(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='✅Yes', callback_data='yes')],])
    await message.answer(
        f"⚙️Here are your settings:\n⏱️ Video speed from {data['speed'][0]} to {data['speed'][1]}\n💨Random noise from {data['noise'][0]} to {data['noise' ][1]}\n🪞Mirror: {'No' if data['mirror?'] == 0 else 'Yes'}\n🤔Do you want to change them?",
        reply_markup=keyboard
    )

@s.callback_query(F.data.contains('yes'))
async def set_settings(callback: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Speed', callback_data='un_speed')],
        [types.InlineKeyboardButton(text='Noise', callback_data='un_rotate')],
        [types.InlineKeyboardButton(text='Mirror', callback_data='un_mirror')]
    ])
    await callback.message.answer("Выберите опцию", reply_markup=keyboard)

@s.callback_query(F.data.startswith('un_'))
async def un_set_settings(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split('un_')[1]
    await callback.answer("Enter numbers in pairs\n strictly with a dot.\nHere's how to do it (example):\n✅1.0 1.2\n🚫0.9 2", show_alert=True)
    if action == 'speed':
        await callback.message.answer('Enter speed range')
        await state.set_state(Speed.speed)
    elif action == 'rotate':
        await callback.message.answer('Enter the noise range in the video')
        await state.set_state(Noise.ns)
    elif action == 'mirror':
        await callback.message.answer('Do you want the following videos to be mirrored?', reply_markup=keyboard)
        await state.set_state(Mirror.mr)

@s.message(Mirror.mr, F.text.in_(choice))
async def mirror(message: types.Message, state: FSMContext):
    if message.text == '✅Yes':
        data['mirror?'] = 1
    elif message.text == '🚫No':
        data['mirror?'] = 0
    with open('jsons/settings.json', 'w') as file:
        json.dump(data, file)
    await message.answer('Changes successfully applied!', reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

@s.message(Mirror.mr)
async def invalid_mirror(message: types.Message, state: FSMContext):
    await message.answer("I don't know such an operation! Try again.", reply_markup=keyboard)

@s.message(Speed.speed)
async def speed(message: types.Message, state: FSMContext):
    temp = [float(i) for i in message.text.split()]
    data['speed'] = temp
    with open('jsons/settings.json', 'w') as file:
        json.dump(data, file)
    await message.answer('Done!')
    await state.clear()

@s.message(Noise.ns)
async def rotate(message: types.Message, state: FSMContext):
    temp = [float(i) for i in message.text.split()]
    data['noise'] = temp
    with open('jsons/settings.json', 'w') as file:
        json.dump(data, file)
    await message.answer('Done!')
    await state.clear()
