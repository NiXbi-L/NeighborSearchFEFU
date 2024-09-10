from DB import DBfunc

async def DELLfriend(userid):
    await DBfunc.DELETEWHERE('friend', f'userid = {userid}')

async def DELLquestionnaire(userid):
    await DBfunc.DELETEWHERE('questionnaire_liked', f'userid = {userid}')
    questionnaire = await DBfunc.SELECT('id', 'questionnaire', f'userid = {userid}')
    if len(questionnaire) != 0:
        await DBfunc.DELETEWHERE('questionnaire_liked', f'qid = {questionnaire[0][0]}')
    await DBfunc.DELETEWHERE('questionnaire', f'userid = {userid}')

async def DELLq_like(message, data):
    user = await DBfunc.SELECT('id,tgid', 'user', f'tgid = {message.from_user.id}')
    myquestionnaire = await DBfunc.SELECT('id,name', 'questionnaire',
                                              f'userid = {user[0][0]}')
    myquestionnaire = myquestionnaire[0]
    await DBfunc.DELETEWHERE('questionnaire_liked',
                                 f'qid = {myquestionnaire[0]} AND userid = {data[message.from_user.id][0][data[message.from_user.id][1]][1]}')
    await DBfunc.DELETEWHERE('questionnaire_liked',
                                 f'qid = {data[message.from_user.id][0][data[message.from_user.id][1]][0]} AND userid = {user[0][0]}')

async def DELL(userid):
    await DELLfriend(userid)
    await DELLquestionnaire(userid)
    await DBfunc.DELETE('user', f'{userid}')

async def Userlink(message, id):
    user = await DBfunc.SELECT('tgid, username', 'user', f'id = {id}')
    user = user[0]
    name = await DBfunc.SELECT('name', 'questionnaire', f'userid = {id}')
    name = name[0][0]
    if str(user[1]) == 'None':
        await message.answer(
            text=f'Ты можешь написать [{name}](tg://openmessage?user_id={user[0]})',
            parse_mode='Markdown')
    else:
        await message.answer(
            text=f'Ты можешь написать [{name}](https://t.me/{user[1]})',
            parse_mode='Markdown')