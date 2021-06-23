from telethon import TelegramClient, events, sync
import requests
import json
import datetime
import time
import threading
import asyncio
import config


api_id = 3845597
api_hash = '1e445e1bad94628c5939e1ccdcb5da15'
name = 'justi_chasti'
chats = 'chasti_escape'
url = 'http://127.0.0.1:5000/'


now = datetime.datetime.now()
client = TelegramClient('session_name', api_id, api_hash)
client.start()



def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def threeVariables(s):
    x = s.split()
    date = ""
    time = ""
    whattodo = ""
    now = datetime.datetime.now()
    for i in range(len(x)):
        s = x[i]
        if s != "в" and s != "Напомнить" and s != "напомнить" and isInt(s[0]) == False:
            whattodo = whattodo + " " + s
        if isInt(s[0]) == True:
            if s.count(":") > 0:
                time = s
            elif s.count(".") == 0:
                date = str(now)[8:10] + "." + str(now)[5:7]
            elif s.count(".") == 1:
                date = s
    whattodo = whattodo[1:]
    if date == "":
        date = str(now.date())
        date = date.replace("-", ".")
    return whattodo, date, time


def get_message(chat):
    @client.on(events.NewMessage(chats=chat))
    async def normal_handler(event):
        inpmess = event.message.to_dict()['message']
        if inpmess.find('Напомнить') != -1 or inpmess.find('напомнить') != -1:
            remind, date, time = threeVariables(inpmess)
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Content-Encoding': 'utf-8'}
            data = {
                "type": "message",
                "text": remind,
                "date": date,
                "time": time
            }
            answer = requests.post(url, data=json.dumps(data), headers=headers)


def surver(timer):
    while True:
        technical_timer = timer
        now = datetime.datetime.now()
        print("now поменян")
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Content-Encoding': 'utf-8'}
        data = {
            "type": "ask",
            "date": str(now.date()),
            "time": str(now.time())
            }
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        now_time0 = float(str(now.time())[:5].replace(':', '.'))
        print(str(now.time())[3:5])
        if now_time0 + config.upd_time_format_0 > 24.0:
            time.sleep (3600 - int(str(now.time())[3:5])*60)
        time.sleep(timer)


def start_demon():
    timer = threading.Thread(target=surver, args=[config.upd_time_format_1*60])       # создание потока-демона для парсинга
    timer.start()

if __name__ == "__main__":
    start_demon()
    get_message(chats)
    client.run_until_disconnected()
