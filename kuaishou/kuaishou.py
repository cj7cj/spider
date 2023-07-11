from fake_useragent import UserAgent
import random
import requests  # 数据请求模块
import re  # 正则表达式模块
import json  # 数据类型处理模块
from tqdm import tqdm  # 进度条配置
import os  # 处理文件和目录
from datetime import date, timedelta
import pandas as pd

today_date = (date.today() + timedelta(days=0)).strftime("%y%m%d")  # 读取今天的日期

ua = UserAgent()

headers = {
    'Content-Type': 'application/json',
    'Cookie': 'kpf=PC_WEB; clientid=3; did=web_bf3927e5bc13e18ab1bd1b46f5770d41; userId=2906121638; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABrRPgB9AvwZ7lfhHAc2pXIJ5kYnzeXrEpZ4jxqkdTGHiD-gvg0Iu6T82kJzjDFD9TRMIPl1Yhe3eeEZKnZo6S4MDuHlDzsHGsLcEjpSVLMXzkAZhmRcI5d0Q7Fl2R5uC7AoQF_Lnny4yZ3VUvwxX5YwQRF0bqUmWvMV8VitdjfHWOKKgM6_lAVvvllsGKKKk7lE_T8qmH6gNYUbDb1NtgZxoSsguEA2pmac6i3oLJsA9rNwKEIiBJnpNXE07Y3wjbuQfcgUJveaHJktWxpHAf6RwC1rqgBSgFMAE; kuaishou.server.web_ph=02045a8e47f6125de45ad04a75ab2d406e8d; kpn=KUAISHOU_VISION',
    'Host': 'www.kuaishou.com',
    'Referer': 'https://www.kuaishou.com/search/video?searchKey=',
    'User-Agent': ua.random
}

url = 'https://www.kuaishou.com/graphql'


if __name__ == "__main__":

    page = 7
    min = 8000
    max = 120000
    dirpath = r'D:/kuaishou/{}'.format(today_date)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        os.mkdir(dirpath + '/csv'.format(today_date))

    index_txt = r'C:\Users\cj\Desktop\ks_index.txt'
    index_list = []
    with open(index_txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            index_list.append(line)

    for num, index in enumerate(tqdm(index_list)):
        try:
            for i in range(page):
                json = {
                    'operationName': "visionSearchPhoto",
                    'query': "fragment photoContent on PhotoEntity {\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  __typename\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    searchSessionId\n    pcursor\n    aladdinBanner {\n      imgUrl\n      link\n      __typename\n    }\n    __typename\n  }\n}\n",
                    'variables': {'keyword': "{}".format(index), 'pcursor': "{}".format(i), 'page': "search"}
                }
                try:
                    response = requests.post(url=url, headers=headers, json=json, timeout=10)
                except Exception as e:
                    print(e)
                    break

                json_data = response.json()
                print(json_data)
                feeds = json_data['data']['visionSearchPhoto']['feeds']
                for feed in feeds:
                    photoUrl = feed['photo']['photoUrl']
                    caption = feed['photo']['caption']
                    duration = feed['photo']['duration']
                    id = feed['photo']['id']
                    if max >= duration >= min:
                        st = pd.DataFrame(
                            {
                                'id': [id],
                                'caption': [caption]
                            }
                        )
                        if os.path.exists(dirpath + '/csv/title.csv'):
                            header = None
                        else:
                            header = ['id', 'caption']

                        st.to_csv(dirpath + '/csv/title.csv', mode='a+', header=header,index=False,
                                  encoding='utf_8_sig')

                        try:
                            video_content = requests.get(url=photoUrl, timeout=10).content
                            open(dirpath + '/' + id + '.mp4', mode='wb').write(video_content)
                        except Exception as e:
                            print(e)
                            break
        except Exception as e:
            print(e)
            pass