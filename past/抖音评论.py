from DrissionPage import ChromiumPage
from DrissionPage.common import Actions
import random
import datetime
import time
import pandas as pd
from tqdm import *

page = ChromiumPage()
page.get("https://www.douyin.com")
input("登陆后回车：")
url = input("请输入要采集视频的url:")
num = int(input("请输入要采集的条数："))

page.get(url)
title = input("请输入文件名称：")
page.listen.start(targets="https://www.douyin.com/aweme/v1/web/comment/list/?")
page.ele('x://*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[2]/div[3]/div/div[2]').click()
nums = 0
info_lists = []
for i in tqdm(range(num // 20 + 1)):
    page.wait(random.randint(1, 2))
    res = page.listen.wait()
    # page.ele('x://*[@id="merge-all-comment-container"]/div/div[3]').click()
    page.actions.move_to('x://*[@id="merge-all-comment-container"]/div/div[3]')
    page.actions.scroll(5000, 0)
    # ac = Actions(page)
    # ac.scroll(2000, 500, ".LvAtyU_f")
    # for i in range(random.randint(1, 4)):
    #     time.sleep(1)
    #     ac.scroll(1000, 200)
    comments = res.response.body["comments"]
    for i in comments:
        name = i["user"]["nickname"]
        ip = i["ip_label"]
        comment = i["text"]
        time = datetime.datetime.fromtimestamp(i["create_time"])
        # 判断是否有图片
        try:
            img = i["image_list"][0]["medium_url"]
            # print(111)
            comment = str(comment) + "【发表图片】"
        except Exception as e:
            # print(222)
            pass
        # 回复数
        reply_comment_total = i["reply_comment_total"]
        # 点赞数
        digg_count=i["digg_count"]
        nums = nums + 1
        info_lists.append([name, ip, comment, time, reply_comment_total,digg_count])
    try:
        if page.ele("text:暂时没有更多评论", timeout=1):
            break
    except Exception as e:
        pass
print("最终采集条数为：", nums)
df = pd.DataFrame(info_lists, columns=['用户名', 'IP', '评论', '时间', "回复数","点赞数"])
df.to_excel(f"{title}.xlsx", index=False)
