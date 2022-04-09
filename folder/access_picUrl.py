import json
import random
import time

import mysql.connector
import requests


def access_cookie():
    with open('./cookie.txt', 'r') as file:
        cookie = file.read()

    return cookie


def access_picUrl():
    url = "https://weibo.com/ajax/profile/getImageWall?uid=6372196907&sinceid=0&has_album=true"

    cookie = access_cookie()

    with mysql.connector.connect(user="root",
                                 password=input('Enter mysql password:'),
                                 host='localhost',
                                 database="Crawler") as db:

        mycursor = db.cursor()

        sinceid = ''

        while True:
            try:
                headers = {
                    "cookie":
                    cookie,
                    "referer":
                    "https://weibo.com/u/6372196907?tabtype=album",
                    "user-agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29"
                }

                response = requests.get(url, headers=headers, timeout=5).text

                dict_response = json.loads(response)

                item_list = dict_response['data']['list']

                for item in item_list:
                    name = item['pid'] + '.jpg'

                    pic_url = f"https://wx3.sinaimg.cn/large/{name}"

                    mycursor.execute(
                        f"INSERT IGNORE Picurl (name, url) VALUES ('{name}', '{pic_url}')"
                    )

                db.commit()

                if sinceid != dict_response['data']['since_id']:
                    sinceid = dict_response['data']['since_id']
                else:
                    print('运行结束')

                    break

                url = f"https://weibo.com/ajax/profile/getImageWall?uid=6372196907&sinceid={sinceid}"

                time.sleep(random.random() * 2)

            except Exception as e:
                print(e)
