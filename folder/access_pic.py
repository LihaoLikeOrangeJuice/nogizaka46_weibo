import asyncio
import time

import mysql.connector
import redis

from . import download


def access_pic(password):
    with mysql.connector.connect(user="root",
                                 password=password,
                                 host="localhost",
                                 database="Crawler") as db:

        mycursor = db.cursor()

        with redis.Redis(host='localhost', port=6379, db=0) as r:

            while True:
                mycursor.execute(f"SELECT * FROM Picurl LIMIT 5;")

                tasks = []

                for info in mycursor:
                    pic_url = info[1]

                    name = info[0]

                    while True:
                        key = r.randomkey()

                        if key != None:
                            proxy = (r.get(key)).decode('utf-8')

                            break

                        time.sleep(10)

                    cor = download.download(pic_url, name, proxy)
                    task = asyncio.ensure_future(cor)
                    tasks.append(task)

                loop = asyncio.get_event_loop()
                result_list = loop.run_until_complete(asyncio.wait(tasks))

                for results in result_list:
                    for result in results:
                        name = result.result()

                        if name != None:
                            mycursor.execute(
                                f"DELETE FROM Picurl WHERE name = '{name}'")

                db.commit()
