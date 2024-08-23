from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from DB import DBfunc

from Handlers.SerchBS.builders import ServiceKeyboard, Gender_INLINE, mainKeyboard2, mainKeyboard
from Handlers.Note.Builders import NoteKeyboard
from Handlers.SerchBS.States import add, reg, Naighbor, Friend
from Handlers.Note.States import Note
from config import BotSetings

router = Router()  # Создаем объект роутер
bot = Bot(token=BotSetings.token)  # Создаем объект бот


@router.message(Command('start'))
async def setname(message: Message, state: FSMContext):
    await state.clear()
    if not (await DBfunc.IF('user', 'id', f'tgid = {message.from_user.id}')):  # проверяем наличие профиля в базе данных
        await message.answer('Для начала работы нужно заполнить профиль. Какого ты пола?',
                             reply_markup=await Gender_INLINE())
        await state.set_state(reg.gender)
    else:
        await message.answer('Выберите сервис которым хотите воспользоваться', reply_markup=await ServiceKeyboard())


async def gender(call: CallbackQuery, state: FSMContext):
    if str(call.from_user.username) != 'None':
        await DBfunc.INSERT('user', 'tgid,username,gender',
                            f'{call.from_user.id},"{call.from_user.username}","{call.data}"')
    else:
        await DBfunc.INSERT('user', 'tgid,gender',
                            f'{call.from_user.id},"{call.data}"')
    await call.message.answer('Профиль создан. Теперь ты можешь пользоваться доступными сервисами',
                              reply_markup=await ServiceKeyboard())
    await state.clear()


@router.message(lambda mesage: mesage.text == 'Поиск соседа')
async def NeighborSearch(message: Message, state: FSMContext):
    await state.set_state(Naighbor.Naighbor)
    await message.answer('Переход к сервису поиска соседа', reply_markup=await mainKeyboard())


@router.message(lambda mesage: mesage.text == 'Поиск друзей')
async def FriendSearch(message: Message, state: FSMContext):
    await state.set_state(Friend.menu)
    await message.answer('Переход к сервису поиска друзей', reply_markup=await mainKeyboard())

@router.message(lambda mesage: mesage.text == 'Справочник')
async def FriendSearch(message: Message, state: FSMContext):
    await state.set_state(Note.menu)
    await message.answer('Переход к сервису cправочник', reply_markup=await NoteKeyboard())


@router.message(lambda mesage: mesage.text == 'К списку сервисов')
async def Back(message: Message, state: FSMContext):
    await message.answer('Выберите сервис которым хотите воспользоваться', reply_markup=await ServiceKeyboard())
    await state.clear()