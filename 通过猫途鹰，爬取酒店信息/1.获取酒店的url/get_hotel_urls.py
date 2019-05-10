# coding=utf-8
import json
import pymysql
import random
import requests
import json
import re
import time


class Sprider(object):
    def __init__(self, xici_orderId, urls, outfile_path):
        self.headers = [{'User-Agent': 'Baiduspider+(+http://www.baidu.com/search/spider.html)'},
                        {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'},
                        {'User-Agent': 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)'},
                        {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'},
                        {
                            'User-Agent': 'Mozilla/5.0 (compatible; Yahoo! Slurp China; http://misc.yahoo.com.cn/help.html)'},
                        {
                            'User-Agent': "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)"},
                        {'User-Agent': "iaskspider/2.0(+http://iask.com/help/help_index.html)"},
                        {'User-Agent': "Mozilla/5.0 (compatible; iaskspider/1.0; MSIE 6.0)"},
                        {'User-Agent': "Sogou web spider/3.0(+http://www.sogou.com/docs/help/webmasters.htm#07)"},
                        {'User-Agent': "Sogou Push Spider/3.0(+http://www.sogou.com/docs/help/webmasters.htm#07)"},
                        ]
        self.xici_orderId = xici_orderId
        self.urls = urls
        self.outfile_path = outfile_path

        self.all_hotel_urls = []

        self.sprider_urls()

    def save_one_time(self, arr, way='a'):
        # 以存数据库的一条为一行（即一个一维数组为一行）

        # 如果是二维数组（多维数组），一般我最多传2维
        if isinstance(arr[0], list):  # arr[0]是list
            with open(outfile_path, way, encoding='utf-8') as f:
                for one in arr:
                    # 一个一维数组为一行
                    f.write(json.dumps(one, ensure_ascii=False) + '\n')
        else:
            with open(self.outfile_path, way, encoding='utf-8') as f:
                f.write(json.dumps(arr, ensure_ascii=False))

    def get_info(self, html):
        # 规则
        re_hotel_urls = r'target="_blank" href="(.+?)" id='
        # 根据规则获取信息
        hotel_urls = re.findall(re_hotel_urls, html)

        for i in range(len(hotel_urls)):
            t = hotel_urls[i]
            hotel_urls[i] = 'https://www.tripadvisor.cn' + t

        return hotel_urls

    def change_proxy_header(self):
        header = random.choice(self.headers)
        proxy = {}
        aa = requests.get(url='http://api3.xiguadaili.com/ip/?tid=' + str(
            self.xici_orderId) + '&num=1&delay=1&protocol=https&filter=on')
        aa.close()
        proxy['https'] = aa.text

        return proxy, header

    def sprider_urls(self):
        # 每次随机获取一个代理ip和头部
        proxy, header = self.change_proxy_header()

        length = len(self.urls)
        for i in range(length):
            print('\r 下标%d:长度%d' % (i, length,), end='')
            time.sleep(0.3)
            if i % 300 == 0:
                proxy, header = self.change_proxy_header()

            url = self.urls[i]

            req = ''
            # req有返回值（requests.get连接异常时无返回值），有返回值，也可能为不是正常的页面
            while (req == ''):
                try:
                    # proxies = proxy,
                    req = requests.get(url=url, headers=header, proxies=proxy, timeout=(3, 3))
                # except requests.exceptions.Timeout or requests.exceptions.ProxyError or ConnectionRefusedError or ConnectionResetError or requests.exceptions.ConnectionError or socket.timeout or urllib3.exceptions.ReadTimeoutError as e:
                except Exception as e:
                    # 更换代理池和头部
                    aa = requests.get(
                        url='http://api3.xiguadaili.com/ip/?tid=556723315772516&num=1&delay=1&protocol=https&filter=on')
                    proxy['https'] = aa.text
                    aa.close()
                    header = random.choice(self.headers)
                    print('超时，更换代理和头部', e)
                    # 无req.close()因为此时无返回req

            while (req.status_code != 200):  # 如果没有正常获得数据

                req.close()  # 关闭连接
                # time.sleep(2)
                req = ''
                # req有返回值（requests.get连接异常时无返回值），有返回值，也可能为不是正常的页面
                while (req == ''):
                    try:
                        # proxies = proxy,
                        req = requests.get(url=url, headers=header, proxies=proxy, timeout=(3, 3))
                    # except requests.exceptions.Timeout or requests.exceptions.ProxyError or ConnectionRefusedError or ConnectionResetError or ConnectionRefusedError or requests.exceptions.ConnectionError or socket.timeout or urllib3.exceptions.ReadTimeoutError as e:
                    except Exception as e:
                        # 更换代理池和头部
                        aa = requests.get(
                            url='http://api3.xiguadaili.com/ip/?tid=556723315772516&num=1&delay=1&protocol=https&filter=on')
                        proxy['https'] = aa.text
                        aa.close()
                        header = random.choice(self.headers)
                        print('超时，更换代理和头部', e)
                        # 无req.close()因为此时无返回req
            # 获取源码后，立即关掉连接
            req.close()
            # 获取源码中的信息
            onehtml_hotel_urls = self.get_info(req.text)

            self.all_hotel_urls.extend(onehtml_hotel_urls)

            # 如果存储的条目大于100或者是最后一个url，就保存一次
            if len(self.all_hotel_urls) >= 100 or i == length - 1:
                self.save_one_time(self.all_hotel_urls, way='a')
                self.all_hotel_urls.clear()  # 清空


def get_all_city_hotel_pageUrls(all_city_hotel_infoes):
    all_city_hotel_pageUrls = []
    for i in range(len(all_city_hotel_infoes)):
        print('\r %d:%d' % (i + 1, len(all_city_hotel_infoes)), end='')
        info = all_city_hotel_infoes[i]

        url = info[0]
        now_page_num = info[1]
        max_page_num = info[2]
        print(url, now_page_num, max_page_num)
        while (now_page_num <= max_page_num):
            a = url.split('-')
            b = [a[0], a[1], 'oa' + str(30 * (now_page_num - 1)), a[2], a[3]]
            new_url = '-'.join(b)
            all_city_hotel_pageUrls.append(new_url)
            now_page_num += 1

    return all_city_hotel_pageUrls


if __name__ == '__main__':


    with open('city_hotel_urls_info.txt', 'r', encoding='utf-8') as f:
        all_city_hotel_infoes = json.loads(f.read())
    # 页面的urls，每一个页面有多个urls
    all_city_hotel_pageUrls = get_all_city_hotel_pageUrls(all_city_hotel_infoes)
    all_city_hotel_pageUrls=list((set(all_city_hotel_pageUrls)))

    # 所有酒店urls
    xici_orderId = 556723315772516
    outfile_path = 'all_hotel_urls.txt'
    Sprider(xici_orderId, all_city_hotel_pageUrls, outfile_path)







