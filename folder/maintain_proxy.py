import asyncio
import time

import aiohttp
import redis
import requests
from requests.exceptions import Timeout


async def test_proxy(proxy, timeout):
    headers = {
        "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with await session.get("https://weibo.com/login.php",
                                         headers=headers,
                                         proxy=proxy,
                                         timeout=5) as response:
                status_code = response.status

        if status_code == 200:
            return proxy, timeout

    except Exception as e:
        print(e)


def maintain_proxy():
    with open('./proxy.txt', 'r') as file:
        url = file.read()

    with open('./account_number.txt', 'r') as file:
        account_number = file.read()

    with open('./password.txt', 'r') as file:
        password = file.read()

    index = 0

    with redis.Redis(host='localhost', port=6379, db=0) as r:
        while True:
            try:
                response = requests.get(url, timeout=5)

                get_time = time.time()

                tasks = []

                if response.status_code == 200:
                    for item in response.text.split('\n'):
                        item = item.split(',')

                        proxy = f'http://{account_number}:{password}@{item[0]}'

                        timeout = item[1].replace("\r", "")

                        cor = test_proxy(proxy, timeout)
                        task = asyncio.ensure_future(cor)
                        tasks.append(task)

                    loop = asyncio.get_event_loop()
                    result_list = loop.run_until_complete(asyncio.wait(tasks))

                    for results in result_list:
                        for result in results:
                            result = result.result()

                            if result != None:
                                r.setex(name=f"proxy{index}",
                                        time=int(
                                            int(result[1]) + get_time -
                                            time.time() - 1),
                                        value=result[0])

                                index += 1

                sleep_time = int(10 - time.time() + get_time + 1)

                if sleep_time > 0:
                    time.sleep(sleep_time)

            except Timeout:
                pass

            except Exception as e:
                print(e)

                time.sleep(10)
