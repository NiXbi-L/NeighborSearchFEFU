from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


async def NoteKeyboard():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text='Доступные статьи'),
        KeyboardButton(text='Предложить статью'),
        KeyboardButton(text='К списку сервисов'),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


async def Sections_INLINE(section, pages=False, page=0, Button=0):
    print()
    builder = InlineKeyboardBuilder()
    if pages:
        for i in section:
            builder.add(
                InlineKeyboardButton(
                    text=f'{i[1]}',
                    callback_data=f'S_NULL_{i[0]}'
                ),
            )
    else:
        for i in section:
            builder.add(
                InlineKeyboardButton(
                    text=f'{i[1]}',
                    callback_data=f'S_NULL_{i[0]}'
                ),
            )
        if Button == 0:
            builder.add(
                InlineKeyboardButton(
                    text=f'Следующая страница',
                    callback_data=f'Next_{page}'
                )
            )
        elif Button == 1:
            builder.add(
                InlineKeyboardButton(
                    text=f'Следующая страница',
                    callback_data=f'Next_{page}'
                ),
                InlineKeyboardButton(
                    text=f'Предыдущая страница',
                    callback_data=f'Back_{page}'
                ),
            )
        elif Button == 2:
            builder.add(
                InlineKeyboardButton(
                    text=f'Предыдущая страница',
                    callback_data=f'Back_{page}'
                ),
            )
    builder.adjust(1)
    return builder.as_markup()


async def Article_INLINE(section, pages=False, page=0, Button=0):
    builder = InlineKeyboardBuilder()
    if pages:
        for i in section:
            builder.add(
                InlineKeyboardButton(
                    text=f'{i[1]}',
                    callback_data=f'A_NULL_{i[0]}'
                ),
            )
        builder.add(
            InlineKeyboardButton(
                text=f'К списку разделов',
                callback_data=f'Sections'
            ),
        )
    else:
        for i in section:
            builder.add(
                InlineKeyboardButton(
                    text=f'{i[1]}',
                    callback_data=f'A_NULL_{i[0]}'
                ),
            )
        if Button == 0:
            builder.add(
                InlineKeyboardButton(
                    text=f'Следующая страница',
                    callback_data=f'A_Next_{page}'
                ), InlineKeyboardButton(
                    text=f'К списку разделов',
                    callback_data=f'Sections'
                ),
            )
        elif Button == 1:
            builder.add(
                InlineKeyboardButton(
                    text=f'Следующая страница',
                    callback_data=f'A_Next_{page}'
                ),
                InlineKeyboardButton(
                    text=f'Предыдущая страница',
                    callback_data=f'A_Back_{page}'
                ),
                InlineKeyboardButton(
                    text=f'К списку разделов',
                    callback_data=f'Sections'
                ),
            )
        elif Button == 2:
            builder.add(
                InlineKeyboardButton(
                    text=f'Предыдущая страница',
                    callback_data=f'A_Back_{page}'
                ),
                InlineKeyboardButton(
                    text=f'К списку разделов',
                    callback_data=f'Sections'
                ),
            )
    builder.adjust(1)
    return builder.as_markup()

async def Back_INLINE(sid):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=f'Назад',
            callback_data=f'back_{sid}'
        )
    )
    builder.adjust(1)
    return builder.as_markup()
