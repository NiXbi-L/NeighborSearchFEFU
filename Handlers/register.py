from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from DB import DBfunc

from Handlers.builders import mainKeyboard, Go, Buildings_INLINE, Gender_INLINE, YN
from Handlers.States import add, reg
from config import BotSetings

router = Router()  # Создаем объект роутер
bot = Bot(token=BotSetings.token)  # Создаем объект бот


@router.message(Command('start'))
async def setname(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет я помогу тебе найти идеального соседа.')
    if not (await DBfunc.IF('user', 'id', f'tgid = {message.from_user.id}')):  # проверяем наличие профиля в базе данных
        await message.answer('Для начала работы нужно заполнить профиль. Какого ты пола?',
                             reply_markup=await Gender_INLINE())
        await state.set_state(reg.gender)
    else:
        userid = await DBfunc.SELECT('id', 'user', f'tgid = {message.from_user.id}')
        userid = userid[0][0]
        if not(await DBfunc.IF('questionnaire', 'id', f'userid = {userid}')):
            await message.answer('У тебя еще нет анкеты. Для начала мне нужно знать в какой корпус ты заселяешься.',
                                 reply_markup=await Buildings_INLINE())
            sent_message = await message.answer("Убираю клавиатуру",
                                                reply_markup=ReplyKeyboardRemove())  # Сообщение для удаления клавиатуры
            await bot.delete_message(chat_id=message.chat.id,
                                     message_id=sent_message.message_id)  # Удаляем это сообщение
            await state.set_state(add.buildings)
        else:
            sent_message = await message.answer("Включаю клавиатуру",
                                                reply_markup=ReplyKeyboardRemove())  # Сообщение для удаления клавиатуры
            await bot.delete_message(chat_id=message.chat.id,
                                     message_id=sent_message.message_id)  # Удаляем это сообщение


@router.callback_query(reg.gender)
async def gender(call: CallbackQuery, state: FSMContext):
    if str(call.from_user.username) != 'None':
        await DBfunc.INSERT('user', 'tgid,username,gender',
                            f'{call.from_user.id},"{call.from_user.username}","{call.data}"')
    else:
        await DBfunc.INSERT('user', 'tgid,gender',
                            f'{call.from_user.id},"{call.data}"')
    await call.message.answer('Профиль создан. Приступим к созданию анкеты?', reply_markup=await YN())
    await state.set_state(reg.YNN)


@router.message(reg.YNN)
async def YNТ(message: Message, state: FSMContext):
    if message.text == 'Да':
        await state.set_state(add.buildings)
        await message.answer('Выбери корпус в который заселяешься', reply_markup=await Buildings_INLINE())
        sent_message = await message.answer("Убираю клавиатуру",
                                            reply_markup=ReplyKeyboardRemove())  # Сообщение для удаления клавиатуры
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=sent_message.message_id)  # Удаляем это сообщение
    elif message.text == 'Нет':
        await message.answer('Хорошо. Приходи как надумаешь.', reply_markup=await mainKeyboard())
        await state.clear()
