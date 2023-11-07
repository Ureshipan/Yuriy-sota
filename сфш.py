import asyncio
from characterai import PyAsyncCAI
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


token = 'vk1.a.rl_zP_q_m0BhgbTtYx8j5HyBEamzZOfbfMd9hBO1Lk4qZQm8BbRizkLqTXEI1xrMG_ACeEQZzdPrWyuBayg0alaYs26INtPXh0hvKSNvx90SkW7KizTH0_vXmC_1lXAGYe9sI0vPzUoYp63bFOZDSTWCcv22QpEIwHfG6Gkzjwsq5AWWih3MTiUTVzVKqHocsntFtM-Rqv-XX6VRhKFNKg'
token2 = 'vk1.a.QxqEoP9LpYbRKbBO1adJPXuvYOWmBELWaZHN0RM1SJgbbm3k1xB3bN6zWvR6JNF7UtCjN2H97JpJIOSVcr2X3J8v64jAu4iC-uSHnEIe90goKffH8LyYRd6Ht-6SBSKWc-jmRo1P9mSJKUgsa9OYpNoeJ92yctxcKDSSECOODb2TyF681ZjVRCaN0HV7P7koPhzEWdjDnkqFdozoINbJMg'


def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


vk = vk_api.VkApi(captcha_handler=captcha_handler,
                  token=token)
longpoll = VkLongPoll(vk)


async def main():
    client = PyAsyncCAI('d1e57a70c7f3581b4e5597e6a3c7182f149f86a7')

    char = 'JsWoXNgvU-oFEhoszaB0WrZFGpRx8PLx6E3JMXF5MEw'

    chat = await client.chat2.get_chat(char)

    author = {
        'author_id': chat['chats'][0]['creator_id']
    }

    for event in longpoll.listen():
        id = -1
        message = ''
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                if event.from_chat:
                    from_u = event.user_id
                    msg = event.text.lower()  # последние сообщение пользователя
                    id = event.chat_id  # id беседы в который был ивент
                    print(msg, id)
                    if len(msg) > 1:
                        if msg[0] == '+':
                            uname = vk.method("users.get", {"user_ids": [from_u][1]})[0]['first_name']
                            message = '[' + uname + ']' + msg[1::]
                        else:
                            message = ''
                    else:
                        message = ''
                else:
                    id = -1

        if message != '' and id > 0:
            async with client.connect() as chat2:
                data = await chat2.send_message(
                    char, chat['chats'][0]['chat_id'],
                    message, author
                )

            name = data['turn']['author']['name']
            text = data['turn']['candidates'][0]['raw_content']

            vk.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})

asyncio.run(main())
