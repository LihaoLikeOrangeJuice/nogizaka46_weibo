import asyncio
import time

import mysql.connector
import redis

from . import download


def access_pic(password):
    time.sleep(60)

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

                    proxy = (r.get(r.randomkey())).decode('utf-8')

                    cor = download.download(pic_url, name, proxy)
                    task = asyncio.ensure_future(cor)
                    tasks.append(task)

                loop = asyncio.get_event_loop()
                results = loop.run_until_complete(asyncio.wait(tasks))

                for result in results[0]:
                    name = result.result()

                    if name != None:
                        db.execute(f"DELETE FROM Picurl WHERE name = '{name}'")

                db.commit()
