import aiohttp
import aiofiles


async def download(url, name, proxy):
    headers = {
        "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29"
    }

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, proxy=proxy) as response:
                response = await response.read()

                async with aiofiles.open(f'./pic/{name}', 'wb') as file:
                    await file.write(response)

        print(f"{name}下载完成！")

        return name

    except Exception as e:
        print(e)
