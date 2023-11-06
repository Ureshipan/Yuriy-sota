import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import ApiError

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


#vk = vk_api.VkApi(token=token2, captcha_handler=captcha_handler)
vk = vk_api.VkApi(captcha_handler=captcha_handler,
                  token=token)
longpoll = VkLongPoll(vk)


def sender(id, text): # функция отправления
    vk.method('messages.send', {'chat_id': id, 'message': text, 'random_id' : 0}) # это просто запомнить


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print('eeeey')
        if event.to_me:
            print('tome')
            if event.from_chat:
                from_u = event.user_id
                msg = event.text.lower() # последние сообщение пользователя
                id = event.chat_id #id беседы в который был ивент
                print(msg, id)
                if 'привет' in msg and 'юра' in msg:
                    print('send')
                    sender(id, 'Привет, ' + user_ids[from_u]) # отправляем в sender(id, text) id беседы и текст