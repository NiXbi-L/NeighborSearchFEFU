from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery

from DB import DBfunc
from Handlers.Note.Builders import NoteKeyboard, Sections_INLINE, Article_INLINE, Back_INLINE
from Handlers.Note.States import Note
from config import BotSetings

router = Router()  # Создаем объект роутер
bot = Bot(token=BotSetings.token)  # Создаем объект бот


@router.message(Note.menu, lambda message: message.text == 'Доступные статьи')
async def Section(message: Message):
    section = await DBfunc.SELECT('id,title', 'section', 'id != 0')
    if len(section) <= 28:
        await message.answer('Выберите раздел', reply_markup=await Sections_INLINE(section, True))
    else:
        await message.answer('Выберите раздел', reply_markup=await Sections_INLINE(section[0:28]))


@router.callback_query(Note.menu, lambda query: query.data.startswith('Next_'))
async def Next(call: CallbackQuery):
    page = int(call.data.split('_')[1]) + 1
    section = await DBfunc.SELECT('id,title', 'section', 'id != 0')
    sec = section[28 * page:28 * (page + 1)]
    if len(section[28 * page::]) > 28:
        await bot.edit_message_text('Выберите раздел', message_id=call.message.message_id, chat_id=call.from_user.id,
                                    reply_markup=await Sections_INLINE(sec, page=page, Button=1))
    else:
        await bot.edit_message_text('Выберите раздел', message_id=call.message.message_id, chat_id=call.from_user.id,
                                    reply_markup=await Sections_INLINE(sec, page=page, Button=2))


@router.callback_query(Note.menu, lambda query: query.data.startswith('Back_'))
async def Next(call: CallbackQuery):
    page = int(call.data.split('_')[1]) - 1
    section = await DBfunc.SELECT('id,title', 'section', 'id != 0')
    sec = section[28 * page:28 * (page + 1)]
    if page == 0:
        await bot.edit_message_text('Выберите раздел', message_id=call.message.message_id, chat_id=call.from_user.id,
                                    reply_markup=await Sections_INLINE(sec, page=page, Button=0))
    elif len(section[28 * page::]) > 28:
        await bot.edit_message_text('Выберите раздел', message_id=call.message.message_id, chat_id=call.from_user.id,
                                    reply_markup=await Sections_INLINE(sec, page=page, Button=1))
    else:
        await bot.edit_message_text('Выберите раздел', message_id=call.message.message_id, chat_id=call.from_user.id,
                                    reply_markup=await Sections_INLINE(sec, page=page, Button=2))


@router.callback_query(Note.menu, lambda query: query.data.startswith('A_Next_'))
async def Next(call: CallbackQuery):
    page = int(call.data.split('_')[2]) + 1
    article = await DBfunc.SELECT('id,title', 'article', 'id != 0')
    sec = article[27 * page:27 * (page + 1)]
    if len(article[27 * page::]) > 27:
        await bot.edit_message_text('Выберите раздел', message_id=call.message.message_id, chat_id=call.from_user.id,
                                    reply_markup=await Article_INLINE(sec, page=page, Button=1))
    else:
        await bot.edit_message_text('Выберите раздел', message_id=call.message.message_id, chat_id=call.from_user.id,
                                    reply_markup=await Article_INLINE(sec, page=page, Button=2))


@router.callback_query(Note.menu, lambda query: query.data.startswith('A_Back_'))
async def Next(call: CallbackQuery):
    page = int(call.data.split('_')[2]) - 1
    article = await DBfunc.SELECT('id,title', 'article', 'id != 0')
    sec = article[27 * page:27 * (page + 1)]
    if page == 0:
        await bot.edit_message_text('Выберите раздел', message_id=call.message.message_id, chat_id=call.from_user.id,
                                    reply_markup=await Article_INLINE(sec, page=page, Button=0))
    elif len(article[27 * page::]) > 27:
        await bot.edit_message_text('Выберите раздел', message_id=call.message.message_id, chat_id=call.from_user.id,
                                    reply_markup=await Article_INLINE(sec, page=page, Button=1))
    else:
        await bot.edit_message_text('Выберите раздел', message_id=call.message.message_id, chat_id=call.from_user.id,
                                    reply_markup=await Article_INLINE(sec, page=page, Button=2))


@router.callback_query(Note.menu, lambda query: query.data.startswith('back_'))
async def Back(call: CallbackQuery):
    data = call.data.split('_')
    article = await DBfunc.SELECT('id,title,text', 'article', f'sid = {data[1]}')
    if len(article) <= 27:
        await bot.edit_message_text('Выберите статью', message_id=call.message.message_id,
                                    chat_id=call.from_user.id, reply_markup=await Article_INLINE(article, True))
    else:
        await bot.edit_message_text('Выберите статью', message_id=call.message.message_id,
                                    chat_id=call.from_user.id, reply_markup=await Article_INLINE(article[0:28]))


@router.callback_query(Note.menu, lambda query: query.data == 'Sections')
async def Back(call: CallbackQuery):
    section = await DBfunc.SELECT('id,title', 'section', 'id != 0')
    if len(section) <= 28:
        await bot.edit_message_text('Выберите раздел', message_id=call.message.message_id,
                                    chat_id=call.from_user.id, reply_markup=await Sections_INLINE(section, True))
    else:
        await bot.edit_message_text('Выберите раздел', message_id=call.message.message_id,
                                    chat_id=call.from_user.id, reply_markup=await Sections_INLINE(section[0:28]))


@router.callback_query(Note.menu)
async def Section(call: CallbackQuery):
    data = call.data.split('_')
    if data[0] == 'S':
        article = await DBfunc.SELECT('id,title,text', 'article', f'sid = {data[2]}')
        if len(article) == 0:
            await call.answer('В этом разделе пусто')
        else:
            if len(article) <= 27:
                await bot.edit_message_text('Выберите статью', message_id=call.message.message_id,
                                            chat_id=call.from_user.id, reply_markup=await Article_INLINE(article, True))
            else:
                await bot.edit_message_text('Выберите статью', message_id=call.message.message_id,
                                            chat_id=call.from_user.id, reply_markup=await Article_INLINE(article[0:28]))
    elif data[0] == 'A':
        text = await DBfunc.SELECT('sid,text', 'article', f'id = {data[2]}')
        text = text[0]
        await bot.edit_message_text(f'{text[1]}', message_id=call.message.message_id,
                                    chat_id=call.from_user.id, parse_mode='Markdown',
                                    reply_markup=await Back_INLINE(text[0]))
