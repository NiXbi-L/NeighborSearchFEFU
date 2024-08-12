from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


async def mainKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Просмотр анкет'),
    ),
    builder.add(
        KeyboardButton(text='Заполнить анкету заново'),
    ),
    builder.add(
        KeyboardButton(text='Моя анкета'),
    ),
    builder.add(
        KeyboardButton(text='Удалить анкету'),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

async def Viewing():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='👎'),
    ),
    builder.add(
        KeyboardButton(text='Меню'),
    ),
    builder.add(
        KeyboardButton(text='👍'),
    ),
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)

async def Ok():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Заполнить заново'),
    ),
    builder.add(
        KeyboardButton(text='Круто, оставляем!'),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

async def YN():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Нет'),
    ),
    builder.add(
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

    builder.add(
        InlineKeyboardButton(
                 text='Test',
                 callback_data=f'Test'
            ),
        # InlineKeyboardButton(
        #     text='K1.8',
        #     callback_data=f'K1.8'
        # ),
        # InlineKeyboardButton(
        #     text='K1.9',
        #     callback_data=f'K1.9'
        # ),
        # InlineKeyboardButton(
        #     text='K1.10',
        #     callback_data=f'K1.10'
        # ),
        # InlineKeyboardButton(
        #     text='K1.11',
        #     callback_data=f'K1.11'
        # ),
        # InlineKeyboardButton(
        #     text='K2.1',
        #     callback_data=f'K2.1'
        # ),
        # InlineKeyboardButton(
        #     text='K2.2',
        #     callback_data=f'K2.2'
        # ),
        # InlineKeyboardButton(
        #     text='K2.3',
        #     callback_data=f'K2.3'
        # ),
        # InlineKeyboardButton(
        #     text='K2.4',
        #     callback_data=f'K2.4'
        # ),
        # InlineKeyboardButton(
        #     text='K2.5',
        #     callback_data=f'K2.5'
        # ),
        # InlineKeyboardButton(
        #     text='K2.6',
        #     callback_data=f'K2.6'
        # ),
        # InlineKeyboardButton(
        #     text='K2.7',
        #     callback_data=f'K2.7'
        # ),
        # InlineKeyboardButton(
        #     text='K1',
        #     callback_data=f'K1'
        # ),
        # InlineKeyboardButton(
        #     text='K2',
        #     callback_data=f'K2'
        # ),
        # InlineKeyboardButton(
        #     text='K3',
        #     callback_data=f'K3'
        # ),
        # InlineKeyboardButton(
        #     text='K4',
        #     callback_data=f'K4'
        # ),
        # InlineKeyboardButton(
        #     text='K5',
        #     callback_data=f'K5'
        # ),
        # InlineKeyboardButton(
        #     text='K6',
        #     callback_data=f'K6'
        # ),
        # InlineKeyboardButton(
        #     text='K7',
        #     callback_data=f'K7'
        # ),
        # InlineKeyboardButton(
        #     text='K8',
        #     callback_data=f'K8'
        # ),
        # InlineKeyboardButton(
        #     text='K9',
        #     callback_data=f'K9'
        # ),
        # InlineKeyboardButton(
        #     text='K10',
        #     callback_data=f'K10'
        # ),
        # InlineKeyboardButton(
        #     text='K11',
        #     callback_data=f'K11'
        # ),
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