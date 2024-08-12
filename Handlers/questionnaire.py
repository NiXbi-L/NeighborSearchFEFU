from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputMediaPhoto

from DB import DBfunc

from Handlers.builders import Photos_INLINE, Ok, mainKeyboard, Buildings_INLINE
from Handlers.States import add
from config import BotSetings

router = Router()  # Создаем объект роутер
bot = Bot(token=BotSetings.token)  # Создаем объект бот

data = {}


@router.callback_query(add.buildings)
async def buildings(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)  # Удаляем это сообщение
    await call.message.answer('Хорошо. Теперь мне нужно узнать как тебя зовут.')
    data[call.from_user.id] = [call.data]
    await state.set_state(add.name)


@router.message(add.name)
async def name(message: Message, state: FSMContext):
    await message.answer('Теперь напиши немного о себе')
    data[message.from_user.id].append(message.text)
    await state.set_state(add.AboutMe)


@router.message(add.AboutMe)
async def AboutMe(message: Message, state: FSMContext):
    await message.answer('Если хочешь можешь прислать фотографии', reply_markup=await Photos_INLINE())
    data[message.from_user.id].append(message.text)
    await state.set_state(add.photos)


@router.message(add.photos)  # Запрос фотографий
async def add_photos(message: Message):
    data[message.from_user.id].append(message.photo[-1].file_id)


@router.callback_query(lambda query: query.data == 'Photo')
async def add_photos(call: CallbackQuery, state: FSMContext):
    print(data[call.from_user.id])
    if len(data[call.from_user.id]) < 4:  # Если длинна списка меньше 4 то фотографии небыли добавлены
        await call.message.answer('Вы не отправили не одной фотографии либо они еще не дошли')
    else:
        await bot.delete_message(chat_id=call.from_user.id,
                                 message_id=call.message.message_id)  # Удаляем это сообщение
        await call.message.answer('Вот так выглядит твоя анкета:', reply_markup=await Ok())
        media = []
        photos = data[call.from_user.id][3::]
        for i in range(len(photos)):
            if i == 0:
                media.append(InputMediaPhoto(
                    media=photos[i],
                    caption=f'{data[call.from_user.id][1]}\n{data[call.from_user.id][2]}'))
            else:
                media.append(InputMediaPhoto(
                    media=photos[i]))
        await bot.send_media_group(chat_id=call.from_user.id, media=media)
        await state.set_state(add.Okk)


@router.callback_query(lambda query: query.data == 'NoPhoto')
async def add_photos(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)  # Удаляем это сообщение
    await call.message.answer('Вот так выглядит твоя анкета:', reply_markup=await Ok())
    await call.message.answer(f'{data[call.from_user.id][1]}\n{data[call.from_user.id][2]}')
    await state.set_state(add.Okk)


@router.message(add.Okk, lambda message: message.text == 'Круто, оставляем!')
async def Okk(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,gender', 'user', f'tgid = {message.from_user.id}')
    user = user[0]
    await message.answer('Твоя анкета создана. Удачи в поисках соседа.', reply_markup=await mainKeyboard())
    dt = data[message.from_user.id]
    if len(dt) < 4:  # Если длинна списка меньше 4 то фотографии небыли добавлены
        if await DBfunc.IF('questionnaire', 'id', f'userid = {user[0]}'):  # Удаляем прошлую анкету если она имеется
            ID = await DBfunc.SELECT('id', 'questionnaire', f'userid = {user[0]}')
            ID = ID[0][0]
            await DBfunc.DELETE('questionnaire', f'{ID}')
        await DBfunc.INSERT('questionnaire', 'userid, building, AboutMe, gender, name',
                            f'{user[0]},"{dt[0]}","{dt[2]}","{user[1]}","{dt[1]}"')
        data.pop(message.from_user.id)
    else:
        ph = ''
        for i in dt[3::]:
            ph += f'{i}|'
        if await DBfunc.IF('questionnaire', 'id', f'userid = {user[0]}'):  # Удаляем прошлую анкету если она имеется
            ID = await DBfunc.SELECT('id', 'questionnaire', f'userid = {user[0]}')
            ID = ID[0][0]
            await DBfunc.DELETE('questionnaire', f'{ID}')
        await DBfunc.INSERT('questionnaire', 'userid, building, AboutMe, photos, gender, name',
                            f'{user[0]},"{dt[0]}","{dt[2]}","{ph}","{user[1]}","{dt[1]}"')
        data.pop(message.from_user.id)


@router.message(add.Okk, lambda message: message.text == 'Заполнить заново')
async def Okk(message: Message, state: FSMContext):
    await message.answer('Выбери корпус в котый заселяешься', reply_markup=await Buildings_INLINE())
    await state.set_state(add.buildings)
    sent_message = await message.answer("Убираю клавиатуру",
                                        reply_markup=ReplyKeyboardRemove())  # Сообщение для удаления клавиатуры
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=sent_message.message_id)  # Удаляем это сообщение
    data.pop(message.from_user.id)


@router.message(lambda message: message.text == 'Заполнить анкету заново')
async def Okk(message: Message, state: FSMContext):
    await message.answer('Выбери корпус в котый заселяешься', reply_markup=await Buildings_INLINE())
    await state.set_state(add.buildings)
    sent_message = await message.answer("Убираю клавиатуру",
                                        reply_markup=ReplyKeyboardRemove())  # Сообщение для удаления клавиатуры
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=sent_message.message_id)  # Удаляем это сообщение


@router.message(lambda message: message.text == 'Удалить анкету')
async def Okk(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,gender', 'user', f'tgid = {message.from_user.id}')
    user = user[0]
    if not (await DBfunc.IF('questionnaire', 'id', f'userid = {user[0]}')):
        await message.answer('У вас нет анкеты')
    else:
        ID = await DBfunc.SELECT('id', 'questionnaire', f'userid = {user[0]}')
        ID = ID[0][0]
        await DBfunc.DELETE('questionnaire', f'{ID}')
        await message.answer('Ваша анкета удалена')


@router.message(lambda message: message.text == 'Моя анкета')
async def Okk(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,gender', 'user', f'tgid = {message.from_user.id}')
    user = user[0]
    if not (await DBfunc.IF('questionnaire', 'id', f'userid = {user[0]}')):
        await message.answer('У вас нет анкеты')
    else:
        data = await DBfunc.SELECT('AboutMe, photos, name', 'questionnaire', f'userid = {user[0]}')
        data = data[0]
        AboutMe = data[0]
        name = data[2]
        media = []
        if str(data[1]) != 'None':
            ph = data[1][0:-1].split('|')
            for i in range(len(ph)):
                if i == 0:
                    media.append(InputMediaPhoto(
                        media=ph[i],
                        caption=f'{name}\n{AboutMe}'))
                else:
                    media.append(InputMediaPhoto(
                        media=ph[i]))
            await bot.send_media_group(chat_id=message.from_user.id, media=media)
        else:
            await message.answer(f'{name}\n{AboutMe}')
