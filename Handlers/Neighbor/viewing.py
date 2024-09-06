from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto

from DB import DBfunc

from Handlers.SerchBS.builders import Viewing, mainKeyboard, Buildings_INLINE
from Handlers.SerchBS.States import View, add, Naighbor
from config import BotSetings

router = Router()  # Создаем объект роутер
bot = Bot(token=BotSetings.token)  # Создаем объект бот


async def genlikedstr(userid):
    likes = await DBfunc.SELECT('qid', 'questionnaire_liked',
                                f'userid = {userid}')
    st = '0, '
    for i in likes:
        lik = i[0]
        st += f'{lik}, '
    return st[0:-2]


async def send(message, questionnairess, index=1):
    questionnaires = questionnairess[index]
    ID = questionnaires[0]
    AboutMe = questionnaires[1]
    name = questionnaires[3]
    try:
        media = []
        if str(questionnaires[2]) != 'None':
            if len(f'{name}\n{AboutMe}') > 1023:
                ph = questionnaires[2][0:-1].split('|')
                for i in range(len(ph)):
                    media.append(InputMediaPhoto(
                        media=ph[i]))
                await bot.send_media_group(chat_id=message.from_user.id, media=media)
                await message.answer(f'{name}\n{AboutMe}')
            else:
                ph = questionnaires[2][0:-1].split('|')
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


@router.message(Naighbor.Naighbor, lambda message: message.text == 'Просмотр анкет')
async def viewing(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,gender,qid', 'user', f'tgid = {message.from_user.id}')
    user = user[0]
    if not (await DBfunc.IF('questionnaire', 'id', f'userid = {user[0]}')):
        await message.answer('У вас еще нет анкеты. Давайте ее создадим. Выберите корпус в который заселяетесь.',
                             reply_markup=await Buildings_INLINE())
        await state.set_state(add.buildings)
        sent_message = await message.answer("Убираю клавиатуру",
                                            reply_markup=ReplyKeyboardRemove())  # Сообщение для удаления клавиатуры
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=sent_message.message_id)  # Удаляем это сообщение
    else:
        data = await DBfunc.SELECT('building', 'questionnaire', f'userid = {user[0]}')

        st = await genlikedstr(user[0])

        questionnaires = await DBfunc.SELECT('id, AboutMe, photos, name', 'questionnaire',
                                             f'gender = "{user[1]}" AND building = "{data[0][0]}" AND id >= {user[2]} AND userid != {user[0]} AND id NOT IN({st})')
        if len(questionnaires) == 0:
            await message.answer('Нет подходящих для вас анкет', reply_markup=await mainKeyboard())
        else:
            await message.answer('Переходим в режим просмотра анкет', reply_markup=await Viewing())
            await state.set_state(View.view)
            ID = await send(message, questionnaires, 0)

            await DBfunc.UPDATE('user', f'qid = {ID}', f'{user[0]}')


@router.message(View.view, lambda message: message.text == '👎')
async def viewing(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,gender,qid', 'user', f'tgid = {message.from_user.id}')
    user = user[0]
    data = await DBfunc.SELECT('building', 'questionnaire', f'userid = {user[0]}')

    st = await genlikedstr(user[0])

    questionnaires = await DBfunc.SELECT('id, AboutMe, photos, name', 'questionnaire',
                                         f'gender = "{user[1]}" AND building = "{data[0][0]}" AND id >= {user[2]} AND userid != {user[0]} AND id NOT IN({st})')
    if len(questionnaires) == 1:
        await DBfunc.UPDATE('user', f'qid = 0', f'{user[0]}')
        Questionnaires = await DBfunc.SELECT('id, AboutMe, photos, name', 'questionnaire',
                                             f'gender = "{user[1]}" AND building = "{data[0][0]}" AND id >= 0 AND userid != {user[0]} AND id NOT IN({st})')
        ID = await send(message, Questionnaires, 0)

        await DBfunc.UPDATE('user', f'qid = {ID}', f'{user[0]}')

    else:
        await state.set_state(View.view)
        ID = await send(message, questionnaires)

        await DBfunc.UPDATE('user', f'qid = {ID}', f'{user[0]}')


@router.message(View.view, lambda message: message.text == '👍')
async def viewing(message: Message, state: FSMContext):
    user = await DBfunc.SELECT('id,gender,qid', 'user', f'tgid = {message.from_user.id}')
    user = user[0]
    data = await DBfunc.SELECT('building', 'questionnaire', f'userid = {user[0]}')

    await DBfunc.INSERT('questionnaire_liked', 'userid, qid', f'{user[0]}, {user[2]}')  # закидываем в список лайкнутых
    st = await genlikedstr(user[0])

    questionnaires = await DBfunc.SELECT('id, AboutMe, photos, name', 'questionnaire',
                                         f'gender = "{user[1]}" AND building = "{data[0][0]}" AND id >= {user[2]} AND userid != {user[0]} AND id NOT IN({st})')

    if len(questionnaires) <= 1:
        await DBfunc.UPDATE('user', f'qid = 0', f'{user[0]}')
        Questionnaires = await DBfunc.SELECT('id, AboutMe, photos, name', 'questionnaire',
                                             f'gender = "{user[1]}" AND building = "{data[0][0]}" AND id >= 0 AND userid != {user[0]} AND id NOT IN({st})')
        ID = 0
        if len(Questionnaires) != 0:
            ID = await send(message, Questionnaires, 0)
        else:
            await message.answer('Нет подходящих для вас анкет', reply_markup=await mainKeyboard())
            await state.set_state(Naighbor.Naighbor)
        await DBfunc.UPDATE('user', f'qid = {ID}', f'{user[0]}')
    else:
        await state.set_state(View.view)
        ID = await send(message, questionnaires)
        await DBfunc.UPDATE('user', f'qid = {ID}', f'{user[0]}')


@router.message(View.view, lambda message: message.text == 'Меню')
async def menu(message: Message, state: FSMContext):
    await message.answer('Возвращаю в меню', reply_markup=await mainKeyboard())
    await state.set_state(Naighbor.Naighbor)
