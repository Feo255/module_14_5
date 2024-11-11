from asyncore import dispatcher
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup, default_state
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import sqlite3
from crud_functions import *

api = ''
bot = Bot(token= api)
dp = Dispatcher(bot, storage=MemoryStorage())



kb = ReplyKeyboardMarkup(
    keyboard=[
        [ KeyboardButton(text = 'Информация'),
          KeyboardButton(text = 'Рассчитать')],
        [
            KeyboardButton(text = 'Купить')
        ],
        [
            KeyboardButton(text = 'Регистрация')
        ]
    ], resize_keyboard = True
)


#kb = ReplyKeyboardMarkup(resize_keyboard=True)
#button = KeyboardButton(text = 'Информация')
#button2 = KeyboardButton(text = 'Рассчитать')
#kb.add(button)
#kb.add(button2)

kb2 = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data= 'calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data= 'formulas')
kb2.add(button3)
kb2.add(button4)

kb3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data= 'product_buying'),
         InlineKeyboardButton(text='Product1', callback_data= 'product_buying'),
         InlineKeyboardButton(text='Product2', callback_data= 'product_buying'),
         InlineKeyboardButton(text='Product3', callback_data= 'product_buying'),
         InlineKeyboardButton(text='Product4', callback_data= 'product_buying'),
         InlineKeyboardButton(text='Product5', callback_data= 'product_buying')
         ]
    ]
)

#kb3 = InlineKeyboardMarkup()
#button31 = InlineKeyboardButton(text='Product1', callback_data= 'product_buying')
#button32 = InlineKeyboardButton(text='Product2', callback_data= 'product_buying')
#button33 = InlineKeyboardButton(text='Product3', callback_data= 'product_buying')
#button34 = InlineKeyboardButton(text='Product4', callback_data= 'product_buying')
#kb3.add(button31)
###kb3.add(button32)
#kb3.add(button33)
#kb3.add(button34)

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer("Фрмула расчёта: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")
    await call.answer()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет", reply_markup=kb)

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_weight(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f"Необходимое количество каллорий: {calories}")
    await state.finish()



@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    check_n = is_included(message.text)
    if check_n is False:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя:')
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
        await state.update_data(email=message.text)
        await message.answer('Введите свой возраст:')
        await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
        await state.update_data(age=message.text)
        await message.answer('Введите свой возраст:')
        data = await state.get_data()
        print(data)
        add_user(str(data['username']), str(data['email']), int(data['age']))
        #calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
        await message.answer("Регистрация прошла успешно")
        await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in prod:
        with open('files/4.png', 'rb') as img:
            await message.answer_photo(img,f'Название: {i[1]} | Описание: {i[2]} | Цена: {i[3]*100}')
    await message.answer("Выберите продукт для покупки: ", reply_markup=kb3)

@dp.callback_query_handler(text='product_buying')
async def get_formulas(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)