import os
import json
import time

import requests
from tqdm import tqdm
from lxml import etree


def down_from_url(url, dst):
    try:
        response = requests.get(url, stream=True)
    except:
        try:
            time.sleep(10)
            response = requests.get(url, stream=True)
        except:
            response = requests.get(url, stream=True)
    file_size = int(response.headers['content-length'])  # (2)
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)  # (3)
    else:
        first_byte = 0
    if first_byte >= file_size:  # (4)
        return True

    header = {"Range": f"bytes={first_byte}-{file_size}"}

    size = 0
    pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=dst)

    try:
        req = requests.get(url, headers=header, stream=True)
    except:
        try:
            time.sleep(5)
            req = requests.get(url, headers=header, stream=True)
        except:
            req = requests.get(url, headers=header, stream=True)

    with open(dst, 'ab') as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                size += len(chunk)
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size == size

def main(first_json):
    headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
             "referer":"https://www.xfollow.com/"}
    resp=requests.get(first_json,headers=headers)
    # print(resp.text)
    temp=json.loads(resp.text)
    next=temp[-1]['post'].get('created_at')
    # print(next)
    for temp in temp:
        # print(temp['post'].get('created_at'))
        # print(temp)
        video_url=temp['post']['media'][0].get('url')
        # print(video_url)
        # video_name=video_url.split("?validfrom=")[0].split('/')[-1]
        is_locked=temp.get('is_locked')
        print(is_locked)
        if is_locked!=True:
            # print("ddd")
            video_name = video_url.split("?validfrom=")[0].split('/')[-1]
            # print(video_name)

            times=0
            while times<10:
                times=times+1

                te=down_from_url(video_url,filename+video_name)
                if te:
                    print(video_name+"下载成功！")
                    time.sleep(2)
                    break
        else: print(video_name+"失败跳过！")
    return next


if __name__=='__main__':

    filename="laura-jonesx/"
    if not os.path.exists(filename):
        os.mkdir(filename)

    # first_json = f"https://www.xfollow.com/api/v1/user/{filename}post/public?before_time=2023-07-09T09:07:09%2B0000&limit=18"
    first_json = f"https://www.xfollow.com/api/v1/user/{filename}post/public?limit=18"
    print(first_json)
    # 下面模拟循环，下载其他页面视频
    # json=first_json
    times=0
    while times<10:
        times=times+1
        te=main(first_json) #2023-06-09T03:06:02
        te=te.replace('+0000','')
        first_json=f"https://www.xfollow.com/api/v1/user/{filename}post/public?before_time={te}%2B0000&limit=18"
        print(first_json)






