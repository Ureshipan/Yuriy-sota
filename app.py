from characterai import aiocai, sendCode, authUser
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import asyncio
import logging
import os
import yaml


DB_PATH = 'data/db.yml'


logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/lastest.log', level=logging.DEBUG)


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


def load_yml_data(path, base_form=dict(mail_boxes={}, group_chats={}, personal_chats={})):
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
            with open('vk_key.txt', 'r') as file:
                vk_token = file.read()
            vk = vk_api.VkApi(captcha_handler=captcha_handler,
                              token=vk_token)
            longpoll = VkLongPoll(vk)

            for chat in static_data['group_chats'].keys():
                if static_data['group_chats']['token'] != 0:
                    

        except Exception as e:
            logger.error(f'{e}')

asyncio.run(main())