from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputMediaPhoto

from DB import DBfunc

from Handlers.SerchBS.builders import mainKeyboard, Viewing
from Handlers.SerchBS.States import Naighbor
from config import BotSetings

router = Router()  # Создаем объект роутер
bot = Bot(token=BotSetings.token)  # Создаем объект бот


async def send(message, questionnairess, index=1):
    questionnaires = questionnairess[index]
    ID = questionnaires[0]
    AboutMe = questionnaires[2]
    name = questionnaires[4]
    try:
        media = []
        if str(questionnaires[3]) != 'None':
            if len(f'{name}\n{AboutMe}') > 1023:
                ph = questionnaires[3][0:-1].split('|')
                for i in range(len(ph)):
                    media.append(InputMediaPhoto(
                        media=ph[i]))
                await bot.send_media_group(chat_id=message.from_user.id, media=media)
                await message.answer(f'{name}\n{AboutMe}')
            else:
                ph = questionnaires[3][0:-1].split('|')
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
    return ID


async def genlikedstr(userid, status=-1):
    myquestionnaire = await DBfunc.SELECT('id', 'questionnaire',
                                          f'userid = {userid}')
    myquestionnaire = myquestionnaire[0][0]
    likes = []
    if status == -1:
        likes = await DBfunc.SELECT('userid', 'questionnaire_liked',
                                    f'qid = {myquestionnaire}')
    else:
        likes = await DBfunc.SELECT('userid', 'questionnaire_liked',
                                    f'qid = {myquestionnaire} AND status = {status}')
    st = '0, '
    for i in likes:
        lik = i[0]
        st += f'{lik}, '
    return st[0:-2]


async def genQ(message, user):
    myLikes = await genlikedstr(user[0][0], 0)
    questionnaire_liked = await DBfunc.SELECT('id,userid, AboutMe, photos, name', 'questionnaire',
                                              f'userid IN({myLikes})')

    if len(questionnaire_liked) == 0:
        await message.answer('Вас еще не лайкнули')
        return [False]
    else:
        return [True, questionnaire_liked]


@router.message(Naighbor.Naighbor, lambda message: message.text == 'Меня лайкнули')
async def MeLikes(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id', 'user', f'tgid = {message.from_user.id}')
    try:
        questionnaire_liked = await genQ(message, user)

        if questionnaire_liked[0]:
            questionnaire_liked_F = questionnaire_liked[1]
            await message.answer('Режим просмотра', reply_markup=await Viewing())
            await state.set_state(Naighbor.Mylikes)
            await send(message, questionnaire_liked_F, index=0)
    except:
        await message.answer('У вас нет анкеты')


@router.message(Naighbor.Mylikes, lambda message: message.text == '👍')
async def Next(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,tgid', 'user', f'tgid = {message.from_user.id}')
    myquestionnaire = await DBfunc.SELECT('id,name', 'questionnaire',
                                          f'userid = {user[0][0]}')
    myquestionnaire = myquestionnaire[0]
    questionnaire_liked = await genQ(message, user)
    await DBfunc.UPDATEWHERE('questionnaire_liked', 'status = 1',
                             f'userid = {questionnaire_liked[1][0][1]} AND qid = {myquestionnaire[0]}')
    await DBfunc.INSERT('questionnaire_liked', 'userid,qid, status', f'{user[0][0]}, {questionnaire_liked[1][0][0]}, 1')
    try:
        us = await DBfunc.SELECT('tgid', 'user', f'id = {questionnaire_liked[1][0][1]}')
        if str(message.from_user.username) == 'None':
            await bot.send_message(chat_id=us[0][0],
                text=f'[{myquestionnaire[1]}](tg://openmessage?user_id={message.from_user.id}) лайкнул в ответ.',
                parse_mode='Markdown')
        else:
            await bot.send_message(chat_id=us[0][0],
                text=f'[{myquestionnaire[1]}](https://t.me/{message.from_user.username}) лайкнул в ответ.',
                parse_mode='Markdown')
    except:
        print('Ошибка')

    if questionnaire_liked[0] and len(questionnaire_liked[1]) > 1:
        questionnaire_liked_F = questionnaire_liked[1]

        user = await DBfunc.SELECT('tgid, username', 'user', f'id = {questionnaire_liked_F[0][1]}')
        user = user[0]

        if str(user[1]) == 'None':
            await message.answer(
                text=f'Ты можешь написать [{questionnaire_liked_F[0][4]}](tg://openmessage?user_id={user[0]})',
                parse_mode='Markdown')
        else:
            await message.answer(
                text=f'Ты можешь написать [{questionnaire_liked_F[0][4]}](https://t.me/{user[1]})',
                parse_mode='Markdown')
        await send(message, questionnaire_liked_F, index=1)
    else:
        await state.set_state(Naighbor.Naighbor)
        await message.answer('Возвращаю в меню', reply_markup=await mainKeyboard())


@router.message(Naighbor.Mylikes, lambda message: message.text == '👎')
async def Back(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id', 'user', f'tgid = {message.from_user.id}')
    myquestionnaire = await DBfunc.SELECT('id', 'questionnaire',
                                          f'userid = {user[0][0]}')
    myquestionnaire = myquestionnaire[0][0]
    questionnaire_liked = await genQ(message, user)
    await DBfunc.UPDATEWHERE('questionnaire_liked', 'status = 2',
                             f'userid = {questionnaire_liked[1][0][1]} AND qid = {myquestionnaire}')

    if questionnaire_liked[0] and len(questionnaire_liked[1]) > 1:
        questionnaire_liked_F = questionnaire_liked[1]
        await send(message, questionnaire_liked_F, index=1)
    else:
        await state.set_state(Naighbor.Naighbor)
        await message.answer('Возвращаю в меню', reply_markup=await mainKeyboard())


@router.message(Naighbor.Mylikes, lambda message: message.text == 'Меню')
async def Back(message: Message, state: FSMContext):
    await state.set_state(Naighbor.Naighbor)
    await message.answer('Возвращаю в меню', reply_markup=await mainKeyboard())
