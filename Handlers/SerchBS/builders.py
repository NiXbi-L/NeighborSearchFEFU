from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


async def mainKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Просмотр анкет'),
        KeyboardButton(text='Заполнить анкету заново'),
        KeyboardButton(text='Моя анкета'),
        KeyboardButton(text='Удалить анкету'),
        KeyboardButton(text='Мои лайки'),
        KeyboardButton(text='Меня лайкнули'),
        KeyboardButton(text='К списку сервисов'),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


async def mainKeyboard2():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Просмотр анкет'),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

async def ServiceKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Поиск соседа'),
        KeyboardButton(text='Поиск друзей'),
        KeyboardButton(text='Справочник'),
    #   KeyboardButton(text='Напоминания'),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)




async def Viewing():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='👎'),
        KeyboardButton(text='Меню'),
        KeyboardButton(text='👍'),
    ),
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)


async def MyLike():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='⬅️'),
        KeyboardButton(text='Меню'),
        KeyboardButton(text='➡️'),
        KeyboardButton(text='Отозвать лайк'),
    )
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)


async def Ok():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Заполнить заново'),
        KeyboardButton(text='Круто, оставляем!'),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


async def YN():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Нет'),
        KeyboardButton(text='Да'),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


async def Go():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Поехали!'),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


async def Buildings_INLINE():
    builder = InlineKeyboardBuilder()
    korp = [1.8, '1.10', 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 6.1, 6.2, 7.1, 7.2, 8.1, 8.2, 9, 10, 11]
    for i in korp:
        builder.add(
            InlineKeyboardButton(
                text=f'К{i}',
                callback_data=f'К{i}'
            )
        )
    builder.add(
        InlineKeyboardButton(
            text='Назад',
            callback_data=f'Und'
        )
    )
    builder.adjust(3)

    return builder.as_markup()


async def Photos_INLINE():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text='Нажать после отправки',
            callback_data=f'Photo'
        ),
        InlineKeyboardButton(
            text='Продолжить без фото',
            callback_data=f'NoPhoto'
        ),
    )
    builder.adjust(3)

    return builder.as_markup()


async def Gender_INLINE():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text='Мужского',
            callback_data=f'M'
        ),
        InlineKeyboardButton(
            text='Женского',
            callback_data=f'W'
        ),
    )
    builder.adjust(3)

    return builder.as_markup()


async def Und_INLINE():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text='Назад',
            callback_data=f'Und'
        )
    )
    builder.adjust(3)

    return builder.as_markup()


async def admKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Сделать рассылку'),
    ),
    builder.add(
        KeyboardButton(text='Выход'),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


async def Find_INLINE():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text='Парня',
            callback_data=f'Friend'
        ),
        InlineKeyboardButton(
            text='Девушку',
            callback_data=f'G_friend'
        ),
        InlineKeyboardButton(
            text='Неважно',
            callback_data=f'Pohui'
        ),
        InlineKeyboardButton(
            text='Назад',
            callback_data=f'Und'
        )
    )
    builder.adjust(2)

    return builder.as_markup()
