import requests
import json


def send(data):
    try:
        response = requests.post('http://194.67.217.180:8383/server/param', json=data)
        response = json.loads(response.content.decode("utf-8"))
        print(response)
    except Exception as e:
        print(e)

    return True


users = [27390261, 65472004, 226665834, 167315364, 70025022, 34436430,
         108794197, 282580371, 259855747, 352074606, 400738456, 61140744]


def report(msg):
    for user in users:
        send_message(user, msg)


def send_message(chat_id, text):
    try:
        requests.get("https://api.telegram.org/bot297649371:AAH1UxOL-5-f4iYnOZr1mm1i6RbuGUmE_Dc/sendMessage",
                     params={"chat_id": chat_id, "text": text})
    except requests.HTTPError:
        pass
