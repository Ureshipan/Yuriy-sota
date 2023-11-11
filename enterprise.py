import asyncio
from characterai import PyAsyncCAI
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
import copy

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





async def tobfromb(client, char, chat, author, message, chat_id):
    async with client.connect() as chat2:
        data = await chat2.send_message(
            char, chat['chats'][0]['chat_id'],
            message, author
        )

    name = data['turn']['author']['name']
    text = data['turn']['candidates'][0]['raw_content']

    vk.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})


f = open('clients-data.json', "r")
clients_data = json.load(f)
f.close()

f = open('prefixes', 'r')
prefixes = f.read()
f.close()


async def main():
    global clients_data
    while True:
        try:
            vk = vk_api.VkApi(captcha_handler=captcha_handler,
                              token=token2)
            longpoll = VkLongPoll(vk)

            serving_clients = {}
            # Update clients!!***************************************************************************************
            for client in clients_data["chats"]:
                print(client)
                try:
                    if client["chat_id"] in list(serving_clients.keys()):
                        if serving_clients[client["chat_id"]]["char"] != client["char"]:
                            temp_cli = PyAsyncCAI(client["client"])
                            temp_chat = await temp_cli.chat2.get_chat(client["char"])
                            temp_au = {'author_id': temp_chat['chats'][0]['creator_id']}
                            serving_clients[client["chat_id"]] = {
                                "client": copy.deepcopy(temp_cli),
                                "char": copy.deepcopy(client["char"]),
                                "chat": copy.deepcopy(temp_chat),
                                "author": copy.deepcopy(temp_au)
                            }
                    else:
                        temp_cli = PyAsyncCAI(client["client"])
                        temp_chat = await temp_cli.chat2.get_chat(client["char"])
                        temp_au = {'author_id': temp_chat['chats'][0]['creator_id']}
                        serving_clients[client["chat_id"]] = {
                            "client": copy.deepcopy(temp_cli),
                            "char": copy.deepcopy(client["char"]),
                            "chat": copy.deepcopy(temp_chat),
                            "author": copy.deepcopy(temp_au)
                        }
                except Exception as e:
                    print('Ошибка с беседой №' + str(client["chat_id"]))
                    print(e)
                    mes = "С добавлением персонажа в вашу беседу произошла ошибка, " \
                          "напишите пожалуйста моему создателю @ureshipan"
                    vk.method('messages.send', {'chat_id': client["chat_id"], 'message': mes, 'random_id': 0})
            # Update clients!!***************************************************************************************
            for event in longpoll.listen():
                id = -1
                message = ''
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        if event.from_chat:
                            from_u = event.user_id
                            msg = event.text  # последние сообщение пользователя
                            id = event.chat_id  # id беседы в который был ивент
                            print(msg, id)
                            if len(msg) > 1:
                                if msg.lower()[0] in prefixes:
                                    user = vk.method("users.get", {"user_ids": from_u})
                                    name = user[0]['first_name'] + ' ' + user[0]['last_name']
                                    message = '[' + name + ']' + msg[1::]
                                    print('[' + name + ']' + msg[1::])
                                elif msg[:11] == '/Настройка:':
                                    message = ''
                                    nast = msg.split('\n')
                                    clients_data["chats"].append({
                                        "chat_id": id,
                                        "client": nast[1].split(" ")[2],
                                        "char": nast[2].split(" ")[2]
                                    })
                                    f = open('clients-data.json', "w")
                                    json.dump(clients_data, f)
                                    f.close()
                    # Update clients!!***************************************************************************************
                                    for client in clients_data["chats"]:
                                        print(client)
                                        try:
                                            if client["chat_id"] in list(serving_clients.keys()):
                                                if serving_clients[client["chat_id"]]["char"] != client["char"]:
                                                    temp_cli = PyAsyncCAI(client["client"])
                                                    temp_chat = await temp_cli.chat2.get_chat(client["char"])
                                                    temp_au = {'author_id': temp_chat['chats'][0]['creator_id']}
                                                    serving_clients[client["chat_id"]] = {
                                                        "client": copy.deepcopy(temp_cli),
                                                        "char": copy.deepcopy(client["char"]),
                                                        "chat": copy.deepcopy(temp_chat),
                                                        "author": copy.deepcopy(temp_au)
                                                    }
                                            else:
                                                temp_cli = PyAsyncCAI(client["client"])
                                                temp_chat = await temp_cli.chat2.get_chat(client["char"])
                                                temp_au = {'author_id': temp_chat['chats'][0]['creator_id']}
                                                serving_clients[client["chat_id"]] = {
                                                    "client": copy.deepcopy(temp_cli),
                                                    "char": copy.deepcopy(client["char"]),
                                                    "chat": copy.deepcopy(temp_chat),
                                                    "author": copy.deepcopy(temp_au)
                                                }
                                        except Exception as e:
                                            print('Ошибка с беседой №' + str(client["chat_id"]))
                                            print(e)
                                            mes = "С добавлением персонажа в вашу беседу произошла ошибка, " \
                                                  "напишите пожалуйста моему создателю @ureshipan"
                                            vk.method('messages.send', {'chat_id': client["chat_id"], 'message': mes, 'random_id': 0})
                    # Update clients!!***************************************************************************************
                                else:
                                    message = ''
                            else:
                                message = ''
                        else:
                            id = -1
                if message != '' and id in list(serving_clients.keys()):
                    tclient = serving_clients[id]["client"]
                    tchar = serving_clients[id]["char"]
                    tchat = serving_clients[id]["chat"]
                    tauthor = serving_clients[id]["author"]
                    async with tclient.connect() as chat2:
                        data = await chat2.send_message(
                            tchar, tchat['chats'][0]['chat_id'],
                            message, tauthor
                        )

                    name = data['turn']['author']['name']
                    text = data['turn']['candidates'][0]['raw_content']
                    print('[Юра]' + text, id)
                    vk.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})
                elif id not in list(serving_clients.keys()) and id > 0:
                    text = "Привет! Я Юра, и пока я всего лишь железка без личности. Но ты можешь это исправить! " \
                           "Для настройки пришли мне сообщение такого формата:\n" \
                           "-----------\n" \
                           "/Настройка:\n" \
                           "Токен пользователя: ************\n" \
                           "ID персонажа: ************\n" \
                           "-----------\n\n" \
                           "*Откуда взять токен пользователя:\n" \
                           "Открой сайт beta.character.ai и открой инструменты разработчика на F12. " \
                           "Дальше в раздел [Приложение], в нём [Хранилище] >> [Локальное хранилище] и " \
                           "найти переменную [char_token]. Из неё скопировать значение [value] БЕЗ " \
                           "КОВЫЧЕК (длинная рандомная строчка).\n\n" \
                           "*Откуда взять ID персонажа:\n" \
                           "Выберите любого персонажа на сайте и откройте с ним диалог. " \
                           "Скопируйте строчку из адресной строки, начиная после [char=] и заканчивая перед [&source]. " \
                           "Вставляйте в сообщение так же без ковычек!"
                    vk.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})
        except Exception as e:
            print(e)


asyncio.run(main())


s = {
    "chat_id": 12,
    "client": "d1e57a70c7f3581b4e5597e6a3c7182f149f86a7",
    "char": "JsWoXNgvU-oFEhoszaB0WrZFGpRx8PLx6E3JMXF5MEw"
  }