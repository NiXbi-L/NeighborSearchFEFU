from g4f.client import Client


async def gpt(promt):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": f"Тебе нужно побыть в роли модератора сайта знакомств(Поиск друзей в том числе) тебе нужно будет проверить подходит ли анкета чтобы ее увидели другие люди. "
                              f"Если анкета подходит ответь да если не подходит то ответь нет. Ниже напиши почему. Учитывай только эти правила: 1. возрастное ограничение сайта 16+ 2. "
                              f"Анкета должна содержать достаточную информацию 3. Если ты думаешь что анкета не была предоставлена то ответь нет"
                              f"\nВот анкета которую нужно проверить:"
                              f"\n{promt}"},
                  ],
    )
    return str(response.choices[0].message.content)


async def chek(qquestionnaire):
    while True:
        uns = await gpt(qquestionnaire)
        unswer = uns.split('\n')
        print(uns)
        if unswer[0].lower()[0:3] == 'нет':
            return [True, f'{uns[4::]}']
        elif unswer[0].lower()[0:2] == 'да':
            return [False, f'{uns[3::]}']
