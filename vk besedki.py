import vk_api
import json

token = 'vk1.a.QxqEoP9LpYbRKbBO1adJPXuvYOWmBELWaZHN0RM1SJgbbm3k1xB3bN6zWvR6JNF7UtCjN2H97JpJIOSVcr2X3J8v64jAu4iC-uSHnEIe90goKffH8LyYRd6Ht-6SBSKWc-jmRo1P9mSJKUgsa9OYpNoeJ92yctxcKDSSECOODb2TyF681ZjVRCaN0HV7P7koPhzEWdjDnkqFdozoINbJMg'

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

index = 1

while True:
    try:
        chat_info = vk.messages.getChat(chat_id=index)
        data = json.load(open('data.json', encoding='utf-8'))
        srt_info = {'title': f'{chat_info["title"]}', 'id': f'{chat_info["id"]}'}
        data['conversations'].append(srt_info)
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        file.close()
        index += 1
    except Exception as e:
        print(repr(e))