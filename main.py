import asyncio
from characterai import PyAsyncCAI


token = 'vk1.a.rl_zP_q_m0BhgbTtYx8j5HyBEamzZOfbfMd9hBO1Lk4qZQm8BbRizkLqTXEI1xrMG_ACeEQZzdPrWyuBayg0alaYs26INtPXh0hvKSNvx90SkW7KizTH0_vXmC_1lXAGYe9sI0vPzUoYp63bFOZDSTWCcv22QpEIwHfG6Gkzjwsq5AWWih3MTiUTVzVKqHocsntFtM-Rqv-XX6VRhKFNKg'
token2 = 'vk1.a.QxqEoP9LpYbRKbBO1adJPXuvYOWmBELWaZHN0RM1SJgbbm3k1xB3bN6zWvR6JNF7UtCjN2H97JpJIOSVcr2X3J8v64jAu4iC-uSHnEIe90goKffH8LyYRd6Ht-6SBSKWc-jmRo1P9mSJKUgsa9OYpNoeJ92yctxcKDSSECOODb2TyF681ZjVRCaN0HV7P7koPhzEWdjDnkqFdozoINbJMg'
user_ids = {
    354398620: 'Влад',
    50039348: 'Полина',
    242995517: 'Яна',
    445692182: 'Ваня'
}


def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


async def main():
    client = PyAsyncCAI('d1e57a70c7f3581b4e5597e6a3c7182f149f86a7')

    char = input('Enter CHAR: ')

    chat = await client.chat2.get_chat(char)

    author = {
        'author_id': chat['chats'][0]['creator_id']
    }

    while True:
        message = input('You: ')

        async with client.connect() as chat2:
            data = await chat2.send_message(
                char, chat['chats'][0]['chat_id'],
                message, author
            )

        name = data['turn']['author']['name']
        text = data['turn']['candidates'][0]['raw_content']

        print(f"{name}: {text}")


asyncio.run(main())
