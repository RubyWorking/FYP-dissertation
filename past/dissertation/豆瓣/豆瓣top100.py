import requests
import pandas as pd
import re
from lxml import etree

all_information = []

for i in range(0, 100, 25):
    url = f"https://www.douban.com/doulist/123178367/?start={i}&sort=seq&playable=0&sub_type="
    res = requests.get(url=url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"

    })
    selector = etree.HTML(res.text)
    movies_tag = selector.xpath('//div[@class="title"]/a/@href')
    # print(movies_tag)
    # print(len(movies_tag))
    for tag in movies_tag:
        movie_url = tag
        movie_res = requests.get(url=movie_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
        })
        selector = etree.HTML(movie_res.text)
        # 中文名
        title = selector.xpath('//*[@id="content"]/h1/span[1]/text()')[0]
        # print(title)
        # 英文名
        try:
            en_name = re.findall('<span class="pl">又名:</span> (.*?)<br/>', movie_res.text)[0]
            # print(en_name)
        except Exception as e:
            en_name="NONE"
        # 首播时间
        time = selector.xpath('//span[@property="v:initialReleaseDate"]/text()')[0]
        # print(time)
        # nums
        nums = selector.xpath('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/a/span/text()')[0]
        # print(nums)
        print(f"中文名：{title}, 英文名：{en_name}, 首播时间：{time}, 评价人数：{nums}")
        all_information.append([title, en_name, time, nums])
df = pd.DataFrame(all_information, columns=['中文名', '英文名', '首发时间', '评论人数'])
df.to_excel("豆瓣top100电视剧.xlsx", index=False, )
