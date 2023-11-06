import g4f
import datetime

mess = []
#key = 'sk-FceW93CGmcTKsULYg26SVGhlQi5BSQwsVQVANolRgXiLIRO3'


def send_no_context(mes):
    global mess
    mess.append({'role': 'user', 'content': mes})
    if len(mess) > 20:
        mess.pop(0)
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo,
        provider=g4f.Provider.ChatgptAi,
        messages=mess,
    )
    mess.append({'role': 'assistant', 'content': response})
    print('Юра Сотов >> ' + response)
    print("[Отправлено в " + str(datetime.datetime.now()) + "]")


print('Юра в сети')
while True:
    mes = input('Влад Типтев >> ')
    print("[Отправлено в " + str(datetime.datetime.now()) + "]")
    send_no_context(mes)