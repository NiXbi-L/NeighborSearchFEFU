from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputMediaPhoto

from DB import DBfunc

from Handlers.SerchBS.builders import Photos_INLINE, Ok, mainKeyboard, Find_INLINE, Und_INLINE
from Handlers.SerchBS.States import Friend
from config import BotSetings
from Handlers.Friends.GPTmoderation import chek

router = Router()  # Создаем объект роутер
bot = Bot(token=BotSetings.token)  # Создаем объект бот

data = {}


@router.callback_query(Friend.buildings, lambda query: query.data == 'Und')
async def buildingsUND(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)  # Удаляем это сообщение
    await call.message.answer('Возвращаю в меню', reply_markup=await mainKeyboard())
    await state.set_state(Friend.menu)


@router.callback_query(Friend.name, lambda call: call.data == 'Und')
async def UND(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)  # Удаляем это сообщение
    await call.message.answer('Кого ищем?', reply_markup=await Find_INLINE())
    await state.set_state(Friend.buildings)


@router.callback_query(Friend.AboutMe, lambda call: call.data == 'Und')
async def buildings(call: CallbackQuery, state: FSMContext):
    data[call.from_user.id].pop(-1)
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)  # Удаляем это сообщение
    await call.message.answer('Как тебя зовут', reply_markup=await Und_INLINE())
    await state.set_state(Friend.name)


@router.callback_query(Friend.buildings)
async def buildings(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)  # Удаляем это сообщение
    await call.message.answer('Хорошо. Теперь мне нужно узнать как тебя зовут.', reply_markup=await Und_INLINE())
    data[call.from_user.id] = [call.data]
    await state.set_state(Friend.name)


@router.message(Friend.name)
async def name(message: Message, state: FSMContext):
    await message.answer('Теперь напиши немного о себе', reply_markup=await Und_INLINE())
    data[message.from_user.id].append(message.text)
    await state.set_state(Friend.AboutMe)


@router.message(Friend.AboutMe)
async def AboutMe(message: Message, state: FSMContext):
    data[message.from_user.id].append(message.text)
    if len(message.text) < 1024:
        await message.answer('Если хочешь можешь прислать фотографии', reply_markup=await Photos_INLINE())
        await state.set_state(Friend.photos)
    else:
        await message.answer('Вот так выглядит твоя анкета:', reply_markup=await Ok())
        await message.answer(f'{data[message.from_user.id][1]}\n{data[message.from_user.id][2]}')
        await state.set_state(Friend.Okk)


@router.message(Friend.photos)  # Запрос фотографий
async def add_photos(message: Message):
    data[message.from_user.id].append(message.photo[-1].file_id)


@router.callback_query(Friend.photos, lambda query: query.data == 'Photo')
async def add_photos(call: CallbackQuery, state: FSMContext):
    if len(data[call.from_user.id]) < 4:  # Если длинна списка меньше 4 то фотографии небыли добавлены
        await call.message.answer('Вы не отправили не одной фотографии либо они еще не дошли')
    else:
        TF = await chek(data[call.from_user.id][2])
        dt1 = data[call.from_user.id][1][2].replace('"', '')
        dt2 = data[call.from_user.id][2].replace('"', '')
        if len(dt1) == 0 or len(dt2) == 0:
            await call.message.answer('Введены не корректные даные. Попробуй еще раз')
            await call.message.answer('Кого ищем?', reply_markup=await Find_INLINE())
            await state.set_state(Friend.buildings)
            data.pop(call.from_user.id)
        elif TF[0]:
            await call.message.answer(f'Выша анкета отклонена:\n{TF[1]}')
            await call.message.answer('Кого ищем?', reply_markup=await Find_INLINE())
            await state.set_state(Friend.buildings)
            data.pop(call.from_user.id)
        else:
            try:
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
                await state.set_state(Friend.Okk)
            except:
                await call.message.answer('Вот так выглядит твоя анкета:', reply_markup=await Ok())
                await call.message.answer(f'{dt1}\n{dt2}')
                await state.set_state(Friend.Okk)


@router.callback_query(Friend.photos, lambda query: query.data == 'NoPhoto')
async def add_photos(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)  # Удаляем это сообщение
    dt1 = data[call.from_user.id][1].replace('"', '')
    dt2 = data[call.from_user.id][2].replace('"', '')
    await call.message.answer('Анкета проверяется ИИ. Ожидайте.')
    TF = await chek(data[call.from_user.id][2])
    print(TF)
    if len(dt1) == 0 or len(dt2) == 0:
        await call.message.answer('Введены не корректные даные. Попробуй еще раз')
        await call.message.answer('Кого ищем?', reply_markup=await Find_INLINE())
        await state.set_state(Friend.buildings)
        data.pop(call.from_user.id)
    elif TF[0]:
        await call.message.answer(f'Выша анкета отклонена:\n{TF[1]}')
        await call.message.answer('Заполните анкету заново.')
        await call.message.answer('Кого ищем?', reply_markup=await Find_INLINE())
        await state.set_state(Friend.buildings)
        data.pop(call.from_user.id)
    else:
        await call.message.answer('Вот так выглядит твоя анкета:', reply_markup=await Ok())
        await call.message.answer(f'{dt1}\n{dt2}')
        await state.set_state(Friend.Okk)


@router.message(Friend.Okk, lambda message: message.text == 'Круто, оставляем!')
async def Okk(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,gender', 'user', f'tgid = {message.from_user.id}')
    user = user[0]
    await message.answer('Твоя анкета создана. Удачи в поисках.', reply_markup=await mainKeyboard())
    await DBfunc.UPDATEWHERE('user', 'qidf = 0', f'tgid = {message.from_user.id}')
    await state.set_state(Friend.menu)
    dt = data[message.from_user.id]
    if len(dt) < 4:  # Если длинна списка меньше 4 то фотографии небыли добавлены
        if await DBfunc.IF('friend', 'id', f'userid = {user[0]}'):  # Удаляем прошлую анкету если она имеется
            ID = await DBfunc.SELECT('id', 'friend', f'userid = {user[0]}')
            ID = ID[0][0]
            await DBfunc.DELETE('friend', f'{ID}')
        dt2 = dt[2].replace('"', '')
        dt1 = dt[1].replace('"', '')
        await DBfunc.INSERT('friend', 'userid, Filter, AboutMe, gender, name',
                            f'{user[0]},"{dt[0]}","{dt2}","{user[1]}","{dt1}"')
        data.pop(message.from_user.id)
    else:
        ph = ''
        for i in dt[3::]:
            ph += f'{i}|'
        if await DBfunc.IF('friend', 'id', f'userid = {user[0]}'):  # Удаляем прошлую анкету если она имеется
            ID = await DBfunc.SELECT('id', 'friend', f'userid = {user[0]}')
            ID = ID[0][0]
            await DBfunc.DELETE('friend', f'{ID}')
        await DBfunc.INSERT('friend', 'userid, Filter, AboutMe, photos, gender, name',
                            f'{user[0]},"{dt[0]}","{dt[2]}","{ph}","{user[1]}","{dt[1]}"')
        data.pop(message.from_user.id)


@router.message(Friend.Okk, lambda message: message.text == 'Заполнить заново')
async def Okk(message: Message, state: FSMContext):
    await message.answer('Кого ищем?', reply_markup=await Find_INLINE())
    await state.set_state(Friend.buildings)
    sent_message = await message.answer("Убираю клавиатуру",
                                        reply_markup=ReplyKeyboardRemove())  # Сообщение для удаления клавиатуры
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=sent_message.message_id)  # Удаляем это сообщение
    data.pop(message.from_user.id)


@router.message(Friend.menu, lambda message: message.text == 'Заполнить анкету заново')
async def Okk(message: Message, state: FSMContext):
    await message.answer('Кого ищем?', reply_markup=await Find_INLINE())
    await state.set_state(Friend.buildings)
    sent_message = await message.answer("Убираю клавиатуру",
                                        reply_markup=ReplyKeyboardRemove())  # Сообщение для удаления клавиатуры
    await bot.delete_message(chat_id=message.chat.id,
                             message_id=sent_message.message_id)  # Удаляем это сообщение


@router.message(Friend.menu, lambda message: message.text == 'Удалить анкету')
async def Okk(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,gender', 'user', f'tgid = {message.from_user.id}')
    user = user[0]
    if not (await DBfunc.IF('friend', 'id', f'userid = {user[0]}')):
        await message.answer('У вас нет анкеты')
    else:
        ID = await DBfunc.SELECT('id', 'friend', f'userid = {user[0]}')
        ID = ID[0][0]
        await DBfunc.DELETE('friend', f'{ID}')
        await message.answer('Ваша анкета удалена')


@router.message(Friend.menu, lambda message: message.text == 'Моя анкета')
async def Okk(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,gender', 'user', f'tgid = {message.from_user.id}')
    user = user[0]
    if not (await DBfunc.IF('friend', 'id', f'userid = {user[0]}')):
        await message.answer('У вас нет анкеты')
    else:
        data = await DBfunc.SELECT('AboutMe, photos, name', 'friend', f'userid = {user[0]}')
        data = data[0]
        AboutMe = data[0]
        name = data[2]
        try:
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
        except:
            await message.answer(f'{name}\n{AboutMe}')
