from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputMediaPhoto

from DB import DBfunc

from Handlers.SerchBS.builders import Photos_INLINE, Ok, mainKeyboard, Buildings_INLINE, Und_INLINE
from Handlers.SerchBS.States import add, Naighbor
from Handlers.General_Func import DELLquestionnaire
from config import BotSetings

router = Router()  # Создаем объект роутер
bot = Bot(token=BotSetings.token)  # Создаем объект бот

data = {}


@router.callback_query(add.name, lambda call: call.data == 'Und')
async def UND(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)  # Удаляем это сообщение
    await call.message.answer('Выбери корпус в который заселяешься', reply_markup=await Buildings_INLINE())
    await state.set_state(add.buildings)


@router.callback_query(add.AboutMe, lambda call: call.data == 'Und')
async def buildings(call: CallbackQuery, state: FSMContext):
    data[call.from_user.id].pop(-1)
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)  # Удаляем это сообщение
    await call.message.answer('Как тебя зовут', reply_markup=await Und_INLINE())
    await state.set_state(add.name)


@router.callback_query(add.buildings, lambda call: call.data == 'Und')
async def buildings(call: CallbackQuery, state: FSMContext):
    await state.set_state(Naighbor.Naighbor)
    await call.message.answer('Переход к сервису поиска соседа', reply_markup=await mainKeyboard())


@router.callback_query(add.buildings)
async def buildings(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)  # Удаляем это сообщение
    await call.message.answer('Хорошо. Теперь мне нужно узнать как тебя зовут.', reply_markup=await Und_INLINE())
    data[call.from_user.id] = [call.data]
    await state.set_state(add.name)


@router.message(add.name)
async def name(message: Message, state: FSMContext):
    if len(message.text) > 100:
        await message.answer(f'Вы привысили лимит в 100 символов  на {100 - len(message.text)}')
    else:
        await message.answer('Теперь напиши немного о себе', reply_markup=await Und_INLINE())
        data[message.from_user.id].append(message.text)
        await state.set_state(add.AboutMe)


@router.message(add.AboutMe)
async def AboutMe(message: Message, state: FSMContext):
    data[message.from_user.id].append(message.text)
    if len(message.text) > 3990:
        await message.answer(f'Вы привысили лимит в 3990 символов  на {3990 - len(message.text)}')
    else:
        await message.answer('Если хочешь можешь прислать фотографии', reply_markup=await Photos_INLINE())
        await state.set_state(add.photos)


@router.message(add.photos)  # Запрос фотографий
async def add_photos(message: Message):
    data[message.from_user.id].append(message.photo[-1].file_id)


@router.callback_query(add.photos, lambda query: query.data == 'Photo')
async def add_photos(call: CallbackQuery, state: FSMContext):
    if len(data[call.from_user.id]) < 4:  # Если длинна списка меньше 4 то фотографии небыли добавлены
        await call.message.answer('Вы не отправили не одной фотографии либо они еще не дошли')
    else:
        dt1 = data[call.from_user.id][1].replace('"', '')
        dt2 = data[call.from_user.id][2].replace('"', '')
        if len(dt1) == 0 or len(dt2) == 0:
            await call.message.answer('Введены не корректные даные. Попробуй еще раз')
            await call.message.answer('Выбери корпус в который заселяешься', reply_markup=await Buildings_INLINE())
            await state.set_state(add.buildings)
            data.pop(call.from_user.id)
        else:
            await call.message.answer('Вот так выглядит твоя анкета:', reply_markup=await Ok())
            await bot.delete_message(chat_id=call.from_user.id,
                                     message_id=call.message.message_id)  # Удаляем это сообщение
            try:
                media = []
                photos = data[call.from_user.id][3::]
                if len(f'{dt1}\n{dt2}') > 1023:
                    for i in range(len(photos)):
                        media.append(InputMediaPhoto(
                            media=photos[i]))
                    await bot.send_media_group(chat_id=call.from_user.id, media=media)
                    await call.message.answer(f'{dt1}\n{dt2}')
                else:
                    for i in range(len(photos)):
                        if i == 0:
                            media.append(InputMediaPhoto(
                                media=photos[i],
                                caption=f'{dt1}\n{dt2}'))
                        else:
                            media.append(InputMediaPhoto(
                                media=photos[i]))
                    await bot.send_media_group(chat_id=call.from_user.id, media=media)
                await state.set_state(add.Okk)
            except:
                await call.message.answer(f'{dt1}\n{dt2}')
                await state.set_state(add.Okk)


@router.callback_query(add.photos, lambda query: query.data == 'NoPhoto')
async def add_photos(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)  # Удаляем это сообщение
    dt1 = data[call.from_user.id][1].replace('"', '')
    dt2 = data[call.from_user.id][2].replace('"', '')
    if len(dt1) == 0 or len(dt2) == 0:
        await call.message.answer('Введены не корректные даные. Попробуй еще раз')
        await call.message.answer('Выбери корпус в который заселяешься', reply_markup=await Buildings_INLINE())
        await state.set_state(add.buildings)
        data.pop(call.from_user.id)
    else:
        await call.message.answer('Вот так выглядит твоя анкета:', reply_markup=await Ok())
        await call.message.answer(f'{dt1}\n{dt2}')
        await state.set_state(add.Okk)


@router.message(add.Okk, lambda message: message.text == 'Круто, оставляем!')
async def Okk(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,gender', 'user', f'tgid = {message.from_user.id}')
    user = user[0]
    await message.answer('Твоя анкета создана. Удачи в поисках соседа.', reply_markup=await mainKeyboard())
    await state.set_state(Naighbor.Naighbor)
    dt = data[message.from_user.id]
    if len(dt) < 4:  # Если длинна списка меньше 4 то фотографии небыли добавлены
        if await DBfunc.IF('questionnaire', 'id', f'userid = {user[0]}'):  # Удаляем прошлую анкету если она имеется
            await DELLquestionnaire(user[0])
        dt2 = dt[2].replace('"', '')
        dt1 = dt[1].replace('"', '')
        await DBfunc.INSERT('questionnaire', 'userid, building, AboutMe, gender, name',
                            f'{user[0]},"{dt[0]}","{dt2}","{user[1]}","{dt1}"')
        data.pop(message.from_user.id)
    else:
        dt2 = dt[2].replace('"', '')
        dt1 = dt[1].replace('"', '')
        ph = ''
        for i in dt[3::]:
            ph += f'{i}|'
        if await DBfunc.IF('questionnaire', 'id', f'userid = {user[0]}'):  # Удаляем прошлую анкету если она имеется
            await DELLquestionnaire(user[0])
        await DBfunc.INSERT('questionnaire', 'userid, building, AboutMe, photos, gender, name',
                            f'{user[0]},"{dt[0]}","{dt2}","{ph}","{user[1]}","{dt1}"')
        data.pop(message.from_user.id)


@router.message(add.Okk, lambda message: message.text == 'Заполнить заново')
async def Okk(message: Message, state: FSMContext):
    await message.answer('Выбери корпус в который заселяешься', reply_markup=await Buildings_INLINE())
    await state.set_state(add.buildings)
    sent_message = await message.answer("Убираю клавиатуру",
                                        reply_markup=ReplyKeyboardRemove())  # Сообщение для удаления клавиатуры
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=sent_message.message_id)  # Удаляем это сообщение
    data.pop(message.from_user.id)


@router.message(Naighbor.Naighbor, lambda message: message.text == 'Заполнить анкету заново')
async def Okk(message: Message, state: FSMContext):
    await message.answer('Выбери корпус в который заселяешься', reply_markup=await Buildings_INLINE())
    await state.set_state(add.buildings)
    sent_message = await message.answer("Убираю клавиатуру",
                                        reply_markup=ReplyKeyboardRemove())  # Сообщение для удаления клавиатуры
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=sent_message.message_id)  # Удаляем это сообщение


@router.message(Naighbor.Naighbor, lambda message: message.text == 'Удалить анкету')
async def Okk(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,gender', 'user', f'tgid = {message.from_user.id}')
    user = user[0]
    if not (await DBfunc.IF('questionnaire', 'id', f'userid = {user[0]}')):
        await message.answer('У вас нет анкеты')
    else:
        await DELLquestionnaire(user[0])
        await message.answer('Ваша анкета удалена')


@router.message(Naighbor.Naighbor, lambda message: message.text == 'Моя анкета')
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
        try:
            media = []
            if str(data[1]) != 'None':
                if len(f'{name}\n{AboutMe}') > 1023:
                    ph = data[1][0:-1].split('|')
                    for i in range(len(ph)):
                        media.append(InputMediaPhoto(
                            media=ph[i]))
                    await bot.send_media_group(chat_id=message.from_user.id, media=media)
                    await message.answer(f'{name}\n{AboutMe}')
                else:
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
        except:
            await message.answer(f'{name}\n{AboutMe}')
