from telethon import TelegramClient, events, sync
import requests
import datetime
import time
import json
import config


api_id = 3845597
api_hash = '1e445e1bad94628c5939e1ccdcb5da15'
name = 'justi_chasti'
chat = 'chasti_escape'
url = 'http://127.0.0.1:5000/'

update_time = 60


def send_message(mes):
    client = TelegramClient('session_name0', api_id, api_hash)
    client.start()
    client.send_message(name, mes)
    @client.on(events.NewMessage(pattern='(?i)hi|hello'))
    async def handler(event):
        await event.respond('Hey!')


def analysis():
    while True:
        now = datetime.datetime.now()
        with open('data.json', 'r') as f:
            data = json.load(f)
        if data['message'] == []:
            print(1)
            time.sleep(update_time)
        else:
            updf = float(str(data['upd'])[:5].replace(':', '.'))
            now_time0 = float(str(now.time())[:5].replace(':', '.'))
            if (now_time0 - updf > 0.30) or ((now_time0 < 0.15) and (24.0 - updf + now_time0 > 30)):
                send_message('сервак упал')
                time.sleep(update_time)
            else:
                flag = 0
                time_list = data['time']
                message_list = data['message']
                for i in time_list:
                    k = str(i).replace(':', '.')
                    p = str(now.time())[:5].replace(':', '.')
                    if (float(k) >= float(p)):
                        flag = 1
                if flag == 0:
                    message_list = []
                while len(message_list) != 0:
                    for i in range(len(message_list)):
                        print(str(now.time())[:5], time_list[i])
                        updf = float(str(time_list[i])[:5].replace(':', '.'))
                        now_time0 = float(str(now.time())[:5].replace(':', '.'))
                        if (updf < now_time0):
                            message_list.pop(i)
                            time_list.pop(i)
                            #('элемент был удален', i)
                        elif (updf == now_time0):
                            send_message(message_list[i])
                            message_list.pop(i)
                            time_list.pop(i)
                            print('phase 1')

                    time.sleep(update_time)
                    now = datetime.datetime.now()


if __name__ == "__main__":
    analysis()