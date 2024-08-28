# 豆瓣影评爬虫，可爬全部详细
import time
import random
from DataRecorder import Recorder
from DrissionPage import WebPage
import re


def crawl(id111):
    link = f'https://movie.douban.com/subject/{id111}/reviews?start=1700'
    page.get(link)
    name = page.title
    recorder = Recorder(f'{name}.xlsx', cache_size=100)
    recorder.set.head(("昵称", "时间", "内容", "星级", "有用数", "无用数", "回应数", "ip"))
    number = 0
    for i in range(1, 10001):
        try:
            # print("111", link)
            page.get(link)
        except:
            print("链接访问全部结束！")
        else:
            try:
                div = page.ele('x://*[@id="content"]/div/div[1]/div[1]')
                elements = div.eles('tag:div@@class=main review-item')
            except:
                print("页面内容列表获取失败....")
                break
            else:
                if len(elements) == 0:
                    print("页面内容为0")
                    break
                else:
                    ids = []
                    for element in elements:
                        id_ = element.attr('id')
                        ids.append(id_)
                    recorder.record()
                    try:
                        numbers = re.findall("start=(\d+)", page('后页>').attr('href'))[0]
                        link = f"https://movie.douban.com/subject/{id111}/reviews?start=" + numbers
                        print(link)
                    except:
                        print("下一页地址获取失败")
                        break
                    else:
                        print("下一页地址获取成功：：", link)
                    print("正在获取本页详细信息：")
                    for id in ids:
                        # page.wait(1)
                        try:
                            info_link = f'https://movie.douban.com/review/{id}/'
                            page.get(info_link)
                            nick_name = page.ele(f'x://*[@id="{id}"]/header/a[1]/span', timeout=2).text
                            content = page.ele(f'x://*[@id="link-report-{id}"]', timeout=2).text
                            create_time = page.ele(f'x://*[@id="{id}"]/header/div/span[1]', timeout=2).text
                            score_level = page.ele(f'x://*[@id="{id}"]/header/span[2]', timeout=2).text
                            useful_count = page.ele('@class=btn useful_count ', timeout=2).text.replace('有用', '')
                            useless_count = page.ele('@class=btn useless_count ', timeout=2).text.replace('无用', '')
                            reply_count = page.ele('@class=react-num', timeout=2).text
                            ip = page.eles('x://div[@class="main-meta"]//span', timeout=2)[-1].text
                            # print(ip)
                        except Exception as e:
                            pass
                        else:
                            number += 1
                            print(number, 'id:', id, nick_name, create_time, '内容已经省略....')
                            recorder.add_data((
                                nick_name, create_time, content, score_level, useful_count, useless_count,
                                reply_count, ip))
                    recorder.record()
    recorder.record()


if __name__ == '__main__':
    page = WebPage('d')
    url = 'https://www.douban.com/'
    page.get(url)
    input('登录后回车：')
    # page.set.window.max()
    # page.set.window.hide()
    id111 = input('电影id:')
    crawl(id111=id111)
    # page.quit(force=True)
# url=[34794707,25907063,27180943,24827387，27186313，26617075，35182499]
