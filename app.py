from characterai import aiocai, sendCode, authUser
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import asyncio
import logging
import os
import yaml
import datetime


DB_PATH = 'data/db.yml'

PREFIXES = {
    'talk': ['.', '+', 'yura ', 'юра '],
    'setup': ['/setup', '/настройка'],
    'key': ['/key ', '/ключ']
}

INSTUCT = 'google.com'

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/lastest.log', level=logging.INFO)


def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


def send_token_to_email(email):
    code = sendCode(email)
    return code


def get_token_by_link_and_email(link, email):
    token = authUser(link, email)
    return token


def load_yml_data(path, base_form=dict(group_chats={}, personal_chats={})):
    if os.path.exists(path):
        with open(path, 'r') as file:
            return yaml.safe_load(file)
    else:
        with open(path, 'w') as file:
            yaml.safe_dump(base_form, file)
        return base_form


def save_yml_data(data, path):
    with open(path, 'w') as file:
        yaml.safe_dump(data, file)


async def main():
    static_data = load_yml_data(DB_PATH)
    sessions = {}
    vk_token = ''
    while True:
        try:
            logger.info(f'New cicle')
            with open('vk_key.txt', 'r') as file:
                vk_token = file.read()
            vk = vk_api.VkApi(captcha_handler=captcha_handler,
                              token=vk_token)
            longpoll = VkLongPoll(vk)
            logger.info(f'VK connect succeful, going to cai logic..')
            for chat in static_data['group_chats'].keys():
                chat_d = static_data['group_chats'][chat]
                logger.info(f'Working with group chat {chat} with token {chat_d['token']}')
                if chat_d['token'] != 0:
                    try:
                        client = aiocai.Client(chat_d['token'])
                        user = await client.get_me()
                        try:
                            ai_chat = await client.get_chat(chat_d['char'])
                            sessions[chat] = dict(
                                                client=user,
                                                chat=ai_chat
                                                )
                            logger.info('Session was created succefully')
                        except Exception as e:
                            logger.error(f'{e} With creation connection for this chat')
                            static_data['group_chats'][chat]['errors'] = "Can't get chat with that character, mabe you need to create one."

                        
                    except Exception as e:
                        logger.error(f'{e} for this chat')

            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        if event.from_chat:
                            obrabotka = dict(
                                user_id=event.user_id, 
                                text=event.text, 
                                chat_id=event.chat_id,
                                type='none',
                                prefix='',
                                message='')
                            if len(obrabotka['text']) > 1:
                                if obrabotka['chat_id'] not in static_data['group_chats'].keys():
                                    static_data['group_chats'][obrabotka['chat_id']] = dict(email="", token=0, char="", error="")
                                for typ in PREFIXES.keys():
                                    for prefix in PREFIXES[typ]:
                                        if obrabotka['text'][:len(prefix)].lower() == prefix:
                                            obrabotka['type'] = typ
                                            obrabotka['prefix'] = prefix
                                            break
                                    if obrabotka['type'] != 'none':
                                        break
                                if obrabotka['type'] != 'none':
                                    if obrabotka['type'] == 'talk':
                                        if static_data['group_chats'][obrabotka['chat_id']]['token'] != 0:
                                            user = vk.method("users.get", {"user_ids": obrabotka['user_id']})
                                            name = user[0]['first_name'] + ' ' + user[0]['last_name']
                                            obrabotka['message'] = '{' + name + '}: ' + obrabotka['text'][len(obrabotka['prefix'])::]
                                        else:
                                            mes = f'Вы не произвели мою настройку или во время настройки что то пошло не так, убедитесь что вы следовали [{INSTUCT}|инструкции].'
                                            vk.method('messages.send', {'chat_id': obrabotka["chat_id"], 'message': mes, 'random_id': 0})

                                    elif obrabotka['type'] == 'setup':
                                        tmp_txt = obrabotka['text'].split('\n')
                                        try:
                                            static_data['group_chats'][obrabotka['chat_id']]['email'] = tmp_txt[1].replace(' ', '')
                                            static_data['group_chats'][obrabotka['chat_id']]['char'] = tmp_txt[2].replace(' ', '')
                                            save_yml_data(static_data, DB_PATH)
                                        except Exception as e:
                                            logger.error(f'{obrabotka['chat_id']}|Wrong format of setup message')
                                            mes = f'Проверьте правильность введённой команды, а затем повторите попытку. Для обращения в поддержку:\nВремя-{datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")}\nID чата-{obrabotka["chat_id"]}'
                                            vk.method('messages.send', {'chat_id': obrabotka["chat_id"], 'message': mes, 'random_id': 0})
                                        if static_data['group_chats'][obrabotka['chat_id']]['token'] == 0:
                                            try:
                                                code = sendCode(static_data['group_chats'][obrabotka['chat_id']]['email'])
                                                mes = 'На ваш email отправлено письмо подтверждния от characterAI. Не переходите по ссылке в нём, а скопируйте её и отправьте её мне в формате "/key *****". \n(Ссылка в письме может выглядеть как кнопка, но её всё равно можно скопировать)'
                                                vk.method('messages.send', {'chat_id': obrabotka["chat_id"], 'message': mes, 'random_id': 0})
                                                logger.info(f'{obrabotka['chat_id']}|Message with code is sent to {static_data['group_chats'][obrabotka['chat_id']]['email']}')
                                            except Exception as e:
                                                logger.error(f'{obrabotka['chat_id']}|Message wasnt sent to email {static_data['group_chats'][obrabotka['chat_id']]['email']} due to error {e}')
                                                mes = f'Не удалось отправить код подтверждения на ваш email. Проверьте его правильность и формат команды, а затем повторите попытку. Для обращения в поддержку:\nВремя-{datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")}\nID чата-{obrabotka["chat_id"]}'
                                                vk.method('messages.send', {'chat_id': obrabotka["chat_id"], 'message': mes, 'random_id': 0})

                                    elif obrabotka['type'] == 'key':
                                        if static_data['group_chats'][obrabotka['chat_id']]['email'] != "":
                                            try:
                                                link = obrabotka['text'].split('\n')[-1].split()[-1]
                                                email = static_data['group_chats'][obrabotka['chat_id']]['email']
                                                token = authUser(link, email)
                                                static_data['group_chats'][obrabotka['chat_id']]['token'] = token
                                                save_yml_data(static_data, DB_PATH)
                                                logger.info(f'{obrabotka['chat_id']}|Succefully got token for chat')
                                            except Exception as e:
                                                logger.error(f'{obrabotka['chat_id']}|Cant get token due to {e}')
                                                mes = f'Не удалось авторизовать Вас, проверьте правильность введённых на прошлом этапе данных и повторите попытку позже. Для обращения в поддержку:\nВремя-{datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")}\nID чата-{obrabotka["chat_id"]}'
                                                vk.method('messages.send', {'chat_id': obrabotka["chat_id"], 'message': mes, 'random_id': 0})

        except Exception as e:
            logger.error(f'{e}')

asyncio.run(main())