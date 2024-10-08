from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputMediaPhoto

from DB import DBfunc

from Handlers.SerchBS.builders import mainKeyboard, MyLike
from Handlers.SerchBS.States import Naighbor
from Handlers.General_Func import Userlink, DELLq_like
from config import BotSetings

router = Router()  # Создаем объект роутер
bot = Bot(token=BotSetings.token)  # Создаем объект бот

data = {}


async def send(message, questionnairess, index=1):
    questionnaires = questionnairess[index]
    print(questionnaires)
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
    except Exception as e:
        print(e)
        await message.answer(f'{name}\n{AboutMe}')
    return ID


async def genlikedstr(userid, status=-1):
    likes = []
    if status == -1:
        likes = await DBfunc.SELECT('qid', 'questionnaire_liked',
                                    f'userid = {userid}')
    else:
        likes = await DBfunc.SELECT('qid', 'questionnaire_liked',
                                    f'userid = {userid} AND status = {status}')
    st = '0, '
    for i in likes:
        lik = i[0]
        st += f'{lik}, '
    return st[0:-2]


@router.message(Naighbor.Naighbor, lambda message: message.text == 'Мои лайки')
async def MyLikes(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id', 'user', f'tgid = {message.from_user.id}')
    myLikes = await genlikedstr(user[0][0], 1)
    questionnaire_liked = list(await DBfunc.SELECT('id, userid, AboutMe, photos, name', 'questionnaire',
                                                   f'id IN({myLikes})'))
    myLikes = await genlikedstr(user[0][0], 0)
    for i in list(await DBfunc.SELECT('id, userid, AboutMe, photos, name', 'questionnaire',
                                      f'id IN({myLikes})')):
        questionnaire_liked.append(i)

    if len(questionnaire_liked) == 0:
        await message.answer('У вас нет лайкнутых анкет')
    else:
        data[message.from_user.id] = [questionnaire_liked, 0]
        await message.answer('Режим просмотра', reply_markup=await MyLike())
        await state.set_state(Naighbor.Mylikes)
        await send(message, data[message.from_user.id][0], index=data[message.from_user.id][1])

        myLikes = await genlikedstr(user[0][0], 1)
        if myLikes != '0':
            await Userlink(message, data[message.from_user.id][0][0][1])


@router.message(Naighbor.Mylikes, lambda message: message.text == '➡️')
async def Next(message: Message):
    data[message.from_user.id][1] += 1
    if data[message.from_user.id][1] > len(data[message.from_user.id][0]) - 1:
        data[message.from_user.id][1] = 0
    await send(message, data[message.from_user.id][0], index=data[message.from_user.id][1])

    if await DBfunc.IF('questionnaire_liked', 'id',
                       f'qid = {data[message.from_user.id][0][data[message.from_user.id][1]][0]} AND status = 1'):
        await Userlink(message, data[message.from_user.id][0][data[message.from_user.id][1]][1])


@router.message(Naighbor.Mylikes, lambda message: message.text == '⬅️')
async def Back(message: Message):
    data[message.from_user.id][1] -= 1
    if data[message.from_user.id][1] < 0:
        data[message.from_user.id][1] = len(data[message.from_user.id][0]) - 1
    await send(message, data[message.from_user.id][0], index=data[message.from_user.id][1])

    if await DBfunc.IF('questionnaire_liked', 'id',
                       f'qid = {data[message.from_user.id][0][data[message.from_user.id][1]][0]} AND status = 1'):
        await Userlink(message, data[message.from_user.id][0][data[message.from_user.id][1]][1])


@router.message(Naighbor.Mylikes, lambda message: message.text == 'Отозвать лайк')
async def UnLike(message: Message, state: FSMContext):
    await DELLq_like(message, data)

    data[message.from_user.id][0].pop(data[message.from_user.id][1])

    if len(data[message.from_user.id][0]) != 0:
        await send(message, data[message.from_user.id][0], index=data[message.from_user.id][1])

        if await DBfunc.IF('questionnaire_liked', 'id',
                           f'qid = {data[message.from_user.id][0][data[message.from_user.id][1]][0]} AND status = 1'):
            await Userlink(message, data[message.from_user.id][0][0][1])
    else:
        await state.set_state(Naighbor.Naighbor)

        await message.answer('Возвращаю в меню', reply_markup=await mainKeyboard())
        data.pop(message.from_user.id)


@router.message(Naighbor.Mylikes, lambda message: message.text == 'Меню')
async def Back(message: Message, state: FSMContext):
    await state.set_state(Naighbor.Naighbor)
    await message.answer('Возвращаю в меню', reply_markup=await mainKeyboard())
    data.pop(message.from_user.id)
