from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto

from DB import DBfunc

from Handlers.SerchBS.builders import Viewing, mainKeyboard, Find_INLINE
from Handlers.SerchBS.States import Friend
from config import BotSetings

router = Router()  # Создаем объект роутер
bot = Bot(token=BotSetings.token)  # Создаем объект бот


@router.message(Friend.menu, lambda message: message.text == 'Просмотр анкет')
async def viewing(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,gender,qidf', 'user', f'tgid = {message.from_user.id}')
    user = user[0]
    if not (await DBfunc.IF('friend', 'id', f'userid = {user[0]}')):
        await message.answer('У вас еще нет анкеты. Кого ищем?',
                             reply_markup=await Find_INLINE())
        await state.set_state(Friend.buildings)
        sent_message = await message.answer("Убираю клавиатуру",
                                            reply_markup=ReplyKeyboardRemove())  # Сообщение для удаления клавиатуры
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=sent_message.message_id)  # Удаляем это сообщение
    else:
        data = await DBfunc.SELECT('Filter', 'friend', f'userid = {user[0]}')
        friends = ''
        if user[1] == 'M':
            if data[0][0] == 'Pohui':
                friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                              f'(Filter = "{data[0][0]}" OR Filter = "Friend") AND id >= {user[2]} AND userid != {user[0]}')
            elif data[0][0] == 'Friend':
                friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                              f'gender = "M" AND (Filter = "Pohui" OR Filter = "Friend") AND id >= {user[2]} AND userid != {user[0]}')
            elif data[0][0] == 'G_friend':
                friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                              f'gender = "W" AND (Filter = "Pohui" OR Filter = "Friend") AND id >= {user[2]} AND userid != {user[0]}')
        elif user[1] == 'W':
            if data[0][0] == 'Pohui':
                friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                              f'(Filter = "{data[0][0]}" OR Filter = "G_friend") AND id >= {user[2]} AND userid != {user[0]}')
            elif data[0][0] == 'Friend':
                friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                              f'gender = "M" AND (Filter = "Pohui" OR Filter = "G_friend") AND id >= {user[2]} AND userid != {user[0]}')
            elif data[0][0] == 'G_friend':
                friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                              f'gender = "W" AND (Filter = "Pohui" OR Filter = "G_friend") AND id >= {user[2]} AND userid != {user[0]}')

        if len(friends) == 0:
            await message.answer('Нет подходящих для вас анкет', reply_markup=await mainKeyboard())
        else:
            await message.answer('Переходим в режим просмотра анкет', reply_markup=await Viewing())
            await state.set_state(Friend.view)
            friends = friends[0]
            ID = friends[0]
            AboutMe = friends[1]
            name = friends[3]
            try:
                media = []
                if str(friends[2]) != 'None':
                    if len(f'{name}\n{AboutMe}') > 1023:
                        ph = friends[2][0:-1].split('|')
                        for i in range(len(ph)):
                            media.append(InputMediaPhoto(
                                media=ph[i]))
                        await bot.send_media_group(chat_id=message.from_user.id, media=media)
                        await message.answer(f'{name}\n{AboutMe}')
                    else:
                        ph = friends[2][0:-1].split('|')
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

            await DBfunc.UPDATE('user', f'qidf = {ID}', f'{user[0]}')


@router.message(Friend.view, lambda message: message.text == '👎')
async def viewing(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,gender,qidf', 'user', f'tgid = {message.from_user.id}')
    user = user[0]
    data = await DBfunc.SELECT('Filter', 'friend', f'userid = {user[0]}')
    friends = ''
    if user[1] == 'M':
        if data[0][0] == 'Pohui':
            friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                          f'(Filter = "{data[0][0]}" OR Filter = "Friend") AND id >= {user[2]} AND userid != {user[0]}')
        elif data[0][0] == 'Friend':
            friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                          f'gender = "M" AND (Filter = "Pohui" OR Filter = "Friend") AND id >= {user[2]} AND userid != {user[0]}')
        elif data[0][0] == 'G_friend':
            print('Почему блять')
            friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                          f'gender = "W" AND (Filter = "Pohui" OR Filter = "Friend") AND id >= {user[2]} AND userid != {user[0]}')
    elif user[1] == 'W':
        if data[0][0] == 'Pohui':
            friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                          f'(Filter = "{data[0][0]}" OR Filter = "G_friend") AND id >= {user[2]} AND userid != {user[0]}')
        elif data[0][0] == 'Friend':
            friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                          f'gender = "M" AND (Filter = "Pohui" OR Filter = "G_friend") AND id >= {user[2]} AND userid != {user[0]}')
        elif data[0][0] == 'G_friend':
            friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                          f'gender = "W" AND (Filter = "Pohui" OR Filter = "G_friend") AND id >= {user[2]} AND userid != {user[0]}')

    if len(friends) == 1:
        await message.answer('Нет подходящих для вас анкет', reply_markup=await mainKeyboard())
        await DBfunc.UPDATE('user', f'qidf = qidf + 1', f'{user[0]}')
        await state.set_state(Friend.menu)
    else:
        await state.set_state(Friend.view)
        friends = friends[1]
        ID = friends[0]
        AboutMe = friends[1]
        name = friends[3]
        try:
            media = []
            if str(friends[2]) != 'None':
                if len(f'{name}\n{AboutMe}') > 1023:
                    ph = friends[2][0:-1].split('|')
                    for i in range(len(ph)):
                        media.append(InputMediaPhoto(
                            media=ph[i]))
                    await bot.send_media_group(chat_id=message.from_user.id, media=media)
                    await message.answer(f'{name}\n{AboutMe}')
                else:
                    ph = friends[2][0:-1].split('|')
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

        await DBfunc.UPDATE('user', f'qidf = {ID}', f'{user[0]}')


@router.message(Friend.view, lambda message: message.text == '👍')
async def viewing(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,gender,qidf', 'user', f'tgid = {message.from_user.id}')
    user = user[0]
    data = await DBfunc.SELECT('Filter', 'friend', f'userid = {user[0]}')
    friends = ''
    if user[1] == 'M':
        if data[0][0] == 'Pohui':
            friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                          f'(Filter = "{data[0][0]}" OR Filter = "Friend") AND id >= {user[2]} AND userid != {user[0]}')
        elif data[0][0] == 'Friend':
            friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                          f'gender = "M" AND (Filter = "Pohui" OR Filter = "Friend") AND id >= {user[2]} AND userid != {user[0]}')
        elif data[0][0] == 'G_friend':
            friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                          f'gender = "W" AND (Filter = "Pohui" OR Filter = "Friend") AND id >= {user[2]} AND userid != {user[0]}')
    elif user[1] == 'W':
        if data[0][0] == 'Pohui':
            friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                          f'(Filter = "{data[0][0]}" OR Filter = "G_friend") AND id >= {user[2]} AND userid != {user[0]}')
        elif data[0][0] == 'Friend':
            friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                          f'gender = "M" AND (Filter = "Pohui" OR Filter = "G_friend") AND id >= {user[2]} AND userid != {user[0]}')
        elif data[0][0] == 'G_friend':
            friends = await DBfunc.SELECT('id, AboutMe, photos, name', 'friend',
                                          f'gender = "W" AND (Filter = "Pohui" OR Filter = "G_friend") AND id >= {user[2]} AND userid != {user[0]}')

    # Пытаемся отправить анкету
    try:
        sendto = await DBfunc.SELECT('userid', 'friend', f'id = {user[2]}')  # получаем данные tgid лайкнутой анкеты
        sendto = await DBfunc.SELECT('tgid', 'user', f'id = {sendto[0][0]}')
        sendto = sendto[0][0]
        # Отправляем свою анкету
        myfriends = await DBfunc.SELECT('AboutMe, photos, name', 'friend', f'userid = {user[0]}')
        myfriends = myfriends[0]
        AboutMe = myfriends[0]
        name = myfriends[2]
        try:
            media = []
            if str(myfriends[1]) != 'None':
                ph = myfriends[1][0:-1].split('|')
                for i in range(len(ph)):
                    if i == 0:
                        media.append(InputMediaPhoto(
                            media=ph[i],
                            caption=f'{name}\n{AboutMe}'))
                    else:
                        media.append(InputMediaPhoto(
                            media=ph[i]))
                await bot.send_media_group(chat_id=sendto, media=media)
            else:
                await bot.send_message(chat_id=sendto, text=f'{name}\n{AboutMe}')
        except:
            await bot.send_message(chat_id=sendto, text=f'{name}\n{AboutMe}')

        if str(message.from_user.username) == 'None':
            await bot.send_message(chat_id=sendto,
                                   text=f'Ты можешь написать [{name}](tg://openmessage?user_id={message.from_user.id})',
                                   parse_mode='Markdown')
        else:
            await bot.send_message(chat_id=sendto,
                                   text=f'Ты можешь написать [{name}](https://t.me/{message.from_user.username})',
                                   parse_mode='Markdown')
        await message.answer('Ваша анкета отправлена ожидайте ответа')
    except:  # Сообщаем пользователю о неудаче
        await message.answer('Ваша анкета не была доставлена, возможно пользователь заблокировал бота.')



    if len(friends) == 1:
        await message.answer('Нет подходящих для вас анкет', reply_markup=await mainKeyboard())
        await DBfunc.UPDATE('user', f'qidf = qidf + 1', f'{user[0]}')
        await state.set_state(Friend.menu)
    else:
        await state.set_state(Friend.view)
        friends = friends[1]
        ID = friends[0]
        AboutMe = friends[1]
        name = friends[3]
        try:
            media = []
            if str(friends[2]) != 'None':
                if len(f'{name}\n{AboutMe}') > 1023:
                    ph = friends[2][0:-1].split('|')
                    for i in range(len(ph)):
                        media.append(InputMediaPhoto(
                            media=ph[i]))
                    await bot.send_media_group(chat_id=message.from_user.id, media=media)
                    await message.answer(f'{name}\n{AboutMe}')
                else:
                    ph = friends[2][0:-1].split('|')
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

        await DBfunc.UPDATE('user', f'qidf = {ID}', f'{user[0]}')


@router.message(Friend.view, lambda message: message.text == 'Меню')
async def menu(message: Message, state: FSMContext):
    await message.answer('Возвращаю в меню', reply_markup=await mainKeyboard())
    await state.set_state(Friend.menu)
