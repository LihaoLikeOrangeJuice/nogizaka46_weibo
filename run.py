from concurrent.futures import process
import os
from folder import access_picUrl, access_pic, maintain_proxy
import multiprocessing

if __name__ == "__main__":
    folder_path = './pic'
    folder = os.path.exists(folder_path)

    if not folder:
        os.makedirs(folder_path)

    a = input('请分步依次进行\n现在执行第一步还是第二步?[1/2]')

    if a == "1":
        access_picUrl.access_picUrl()
    elif a == "2":
        process = [
            multiprocessing.Process(target=maintain_proxy.maintain_proxy),
            multiprocessing.Process(target=access_pic.access_pic,
                                    args=(input('Enter mysql password:'), ))
        ]

        [p.start() for p in process]
        [p.join() for p in process]