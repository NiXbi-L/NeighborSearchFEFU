from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
import asyncio

from DB import DBfunc

from Handlers.SerchBS.builders import admKeyboard, mainKeyboard, Photos_INLINE, Ok
from Handlers.SerchBS.States import admin
from config import BotSetings

router = Router()  # Создаем объект роутер
bot = Bot(token=BotSetings.token)  # Создаем объект бот
data = {}


async def mailigMethod(users, usid): #Метод рассылки сообщений
    Sended = 0
    Blocked = 0
    for i in users:
        tgid = i[1]
        try:
            if len(data) == 1:
                await bot.send_message(chat_id=tgid, text=f'{data[usid][0]}')
                Sended += 1
            else:
                media = []
                photos = data[usid][1::]
                for i in range(len(photos)):
                    if i == 0:
                        media.append(InputMediaPhoto(
                            media=photos[i],
                            caption=f'{data[usid][0]}'))
                    else:
                        media.append(InputMediaPhoto(
                            media=photos[i]))
                await bot.send_media_group(chat_id=tgid, media=media)
                Sended += 1
        except:
            Blocked += 1
            await DBfunc.DELETEWHERE('questionnaire', f'userid = {i[0]}')
            await DBfunc.DELETEWHERE('friend', f'userid = {i[0]}')
            await DBfunc.DELETE('user', f'{i[0]}')
    await bot.send_message(chat_id=usid, text=f'Отчет по рассылке:\n'
                                              f'Дошло: {Sended}\n'
                                              f'Не дошло: {Blocked}')
    data.pop(usid)


@router.message(Command('adm'), lambda message: message.from_user.id in BotSetings.admin)
async def adm(message: Message, state: FSMContext):
    await state.set_state(admin.admMenu)
    await message.answer('Вы вошли в админ панель. Что хотите сделать?', reply_markup=await admKeyboard())


@router.message(admin.admMenu, lambda message: message.text == 'Выход')
async def exit(message: Message, state: FSMContext):
    await message.answer('Возвращаю в главное меню.', reply_markup=await mainKeyboard())
    await state.clear()


# Создание рассылки
@router.message(admin.admMenu, lambda message: message.text == 'Сделать рассылку')
async def mailing(message: Message, state: FSMContext):
    await message.answer('Введите текст рассылки')
    await state.set_state(admin.text)


@router.message(admin.text)
async def txt(message: Message, state: FSMContext):
    data[message.from_user.id] = [message.text]
    await message.answer('Вы можете прикрипить фотографии', reply_markup=await Photos_INLINE())
    await state.set_state(admin.photos)


@router.message(admin.photos)  # Запрос фотографий
async def add_photos(message: Message):
    data[message.from_user.id].append(message.photo[-1].file_id)


@router.callback_query(admin.photos, lambda query: query.data == 'Photo')
async def add_photos(call: CallbackQuery, state: FSMContext):
    if len(data[call.from_user.id]) == 1:
        await call.message.answer('Вы не отправили не одной фотографии или они еще не дошли')
    else:
        await bot.delete_message(chat_id=call.from_user.id,
                                 message_id=call.message.message_id)  # Удаляем это сообщение
        await call.message.answer('Вот так выглядит сообщение', reply_markup=await Ok())
        media = []
        photos = data[call.from_user.id][1::]
        for i in range(len(photos)):
            if i == 0:
                media.append(InputMediaPhoto(
                    media=photos[i],
                    caption=f'{data[call.from_user.id][0]}'))
            else:
                media.append(InputMediaPhoto(
                    media=photos[i]))
        await bot.send_media_group(chat_id=call.from_user.id, media=media)
        await state.set_state(admin.okk)


@router.callback_query(admin.photos, lambda query: query.data == 'NoPhoto')
async def add_photos(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)  # Удаляем это сообщение
    await call.message.answer('Вот так выглядит сообщение', reply_markup=await Ok())
    await call.message.answer(f'{data[call.from_user.id][0]}')
    await state.set_state(admin.okk)


@router.message(admin.okk, lambda message: message.text == 'Круто, оставляем!')
async def Okk(message: Message, state: FSMContext):
    users = await DBfunc.SELECT('id, tgid', 'user', f'tgid != {message.from_user.id}')
    task = asyncio.create_task(mailigMethod(users, message.from_user.id))
    await message.answer('Рассылка началась. Вам придет отчет как только все сообщения будут доставлены',
                         reply_markup=await admKeyboard())
    await state.set_state(admin.admMenu)


@router.message(admin.okk, lambda message: message.text == 'Заполнить заново')
async def N_Okk(message: Message, state: FSMContext):
    await message.answer('Введите текст рассылки')
    await state.set_state(admin.text)

# Создание рассылки
