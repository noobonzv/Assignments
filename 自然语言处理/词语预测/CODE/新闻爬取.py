# -*- coding: UTF-8 -*-
import json
from bs4 import BeautifulSoup
import requests
import os
import time


def get_one_news(news_infor, n):
    """接受新闻标题和网址，以及已爬取的网页数，返回是否成功保存

    :param news_infor: list，[title, url]
    :return: 成功保存返回True，否则False
    """
    news_url = news_infor[1]
    kv2 = {'user-agent': 'Mozilla/5.0'}
    r2 = requests.get(news_url, headers=kv2)
    r2.raise_for_status()
    r2.encoding = r2.apparent_encoding
    soup = BeautifulSoup(r2.text, "html.parser")
    # 取出正文
    article = []
    for p in soup.select('.article'):
        article.append(p.text.strip().lstrip())
    # 合成字符串
    article_content = ''.join(article)
    # 去掉结尾的不需要的内容，见实验报告
    end = article_content.find('\n\n\n\n\n\n')
    article_content = article_content[:end]
    # 判断开头是否含有汉字，因为有可能存在style，这种就直接放弃
    has_chinese = False
    for char in article_content[:10]:
        if '\u4e00' <= char <= '\u9fff':
            has_chinese = True
            break
    # 保证新闻长于500字
    if has_chinese and len(article_content) > 500:
        print('[', n, '/ 1000 ] ', news_infor)
        # 保存新闻
        filename = str(n) + '.txt'
        cur_path = os.getcwd()
        file_path = cur_path + '\\' + filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(news_infor[0] + '\n')
            f.write(article_content)
        return True
    return False


if __name__ == '__main__':
    news_num = 0
    news_title_url = []
    time_start = time.time()
    # 每页新闻50条，用50页是来保证有足够的新闻
    for page_num in range(1, 50):
        try:
            url = f'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2515&k=&num=50&page={str(page_num)}&r=0.5' \
                f'&callback=jQuery111206769814687743869_1572427017317&_=1572427017314'
            kv = {'user-agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=kv)
            # 解析 json文件
            reply = json.loads(r.text[46:-14])
            # print(len(reply['result']['data']))
            # 处理该页的50条新闻
            for i in range(0, 50):
                news_info = [reply['result']['data'][i]['title'], reply['result']['data'][i]['url']]
                succeed = get_one_news(news_info, news_num)
                # 成功保存才算数
                if succeed:
                    news_num += 1
                    news_title_url.append(news_info)

            if news_num > 1000:
                break
        except:
            print('Something wrong! Ignore it and continue crawl...')
            continue
    time_end = time.time()
    print('Total time cost:', time_end - time_start, 's')