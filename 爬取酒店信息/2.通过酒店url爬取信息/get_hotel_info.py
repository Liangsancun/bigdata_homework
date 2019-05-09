import get_proxies
import get_headers
import random
import requests
import json
import re
import time
import socket

def load_urls(file_path):
    # 返回酒店链接s
    urls = []
    with open(file_path, 'r', encoding='utf-8') as f:
        temp = json.loads(f.read())
    for i in temp:
        urls.append('https://www.tripadvisor.cn'+i)
    return urls

class Sprider(object):
    def __init__(self,proxies,headers,urls):
        self.proxies = proxies
        self.headers = headers
        self.urls = urls

        self.hotels = []
        self.comments = []
        self.near_hotels = []
        self.near_eatings = []
        self.near_scenes = []



    def get_info(self,html,url):

        one_hotel_comments = []

        one_near_hotel = []
        one_near_eating = []
        one_near_scene = []


        # 规则
        re_name = r'<h1 id="HEADING"class="ui_header h1">(.+?)<div'
        re_name_en = r'class="is-hidden-mobile">(.+?)</div>'
        re_discount = r'data-sizegroup="hr_chevron_prices">￥(.+?)</div>'
        re_discount_2 = r'<div class="bb_price_text ">￥(.+?)</div>'
        re_discount_net = r'class="providerImg"  alt="(.+?)" />'
        re_rank = r'class="rank">(.+?)</b>'
        re_comment_count = r'class="reviewCount ">(.+?) 条点评</span>'
        re_comment_count_2 = r'class="reviewCount ui_link level_4">(.+?) 条点评</span>'
        re_grade = r'class="ui_bubble_rating bubble_(.+?)" style='
        re_address_1 = r'<span class="detail ">(.+?)<span class="locality"'
        re_address_2 = r'class="locality">(.+?)</span>'
        re_address_3 = r'<span class="street-address">(.+?)</span>'
        re_address_4 = r'class="postal-code">(.+?)</span></span>'

        re_pic_num = r'class="is-hidden-mobile hotels-media-album-parts-PhotoCount__text--3OXuH">(.+?)</span>'
        re_fea = r'class="entry ui_column is-4-tablet is-6-mobile is-4-desktop"><DIV class="textitem" data-prwidget-name="text" data-prwidget-init="">(.+?)</DIV'
        re_subname = r'<div class="sub_title">别名</div><div class="sub_content"><DIV class="textitem" data-prwidget-name="text" data-prwidget-init="">(.+?)</DIV>'
        re_star = r'class="ui_star_rating star_(.+?)"'
        re_prize = r'class="ui_icon certificate-of-excellence">(.+?)</'
        re_discribe = r'class="introText">(.+?)<span class="seeMore"'
        re_style = r'<DIV class="textitem style" data-prwidget-name="text" data-prwidget-init="">(.+?)</DIV>'
        re_room_style = r'class="sub_title">客房类型</div><div class="sub_content"><DIV class="textitem" data-prwidget-name="text" data-prwidget-init="">(.+?)</DIV>'
        re_have_website = r'class="detail blue_test">(.+?)</span>'
        re_have_email = r'span class="detail">联系酒店</(.+?)>'
        re_near_name = r'class="poiName" dir="auto">(.+?)</'
        re_near_distance = r'class="distance">(.+?)</'
        re_locid = r'data-locid="(.+?)"'
        re_comment_id = r';"id="(.+?)"><span class=\'noQuotes\'>'
        re_stay_hotel_date = r'<span class="stay_date_label">入住日期：</span>(.+?)</DIV>'
        re_comment_date = r'<span class="ratingDate" title=\'(.+?)\' '
        re_comment_title = r'span class=\'noQuotes\'>(.+?)</span>'
        re_comment_context = r'<p class="partial_entry" >(.+?)</p>'
        re_comment_star = r'<div class="ui_column is-9"><span class="ui_bubble_rating bubble_(.+?)'
        re_comment_person = r';"><div>(.+?)</div>'

        hotel_id = url.split('-')[2]
        name = re.findall(re_name, html)[0]
        name_en = re.findall(re_name_en, html)[0]

        discount_1 = re.findall(re_discount, html)

        if len(discount_1) > 0:
            discount_1 = discount_1[0]
        else:
            discount_1 = ''
        discount_2 = re.findall(re_discount_2, html)
        if len(discount_2) > 0:
            discount_2 = discount_2[0]
        else:
            discount_2 = ''
        discount = discount_1 + discount_2

        discount_net = re.findall(re_discount_net, html)

        if len(discount_net) > 0:
            discount_net = discount_net[0]


        else:
            discount_net = '无'
        rank = re.findall(re_rank, html)

        if len(rank) > 0:
            rank = rank[0][3:]
        else:
            rank = '无'

        comment_count = re.findall(re_comment_count, html)
        comment_count_2 = re.findall(re_comment_count_2,html)

        if len(comment_count) > 0:
            comment_count = comment_count[0]
        elif len(comment_count_2)>0:
            comment_count = comment_count_2[0]
        else:
            comment_count = '无'

        grade = re.findall(re_grade, html)
        if len(grade) > 0 and len(grade[0])<3:
            grade = str(int(grade[0]) / 10)
        else:
            grade = '无'

        address_1 = re.findall(re_address_1, html)
        if len(address_1) > 0:
            a = address_1[0]
            if len(a) > 10:
                address_1 = ''
            else:
                address_1 = a
        else:
            address_1 = ''
        address_2 = re.findall(re_address_2, html)[0]
        address_3 = re.findall(re_address_3, html)[0]
        address_4 = re.findall(re_address_4, html)
        if len(address_4) == 0:
            address_4 = ''
        else:
            address_4 = address_4[0]
        address = address_1 + address_2 + address_3 + address_4

        pic_num = re.findall(re_pic_num, html)

        if len(pic_num) > 0:
            pic_num = pic_num[0].split('>')[2].split('<')[0]
        else:
            pic_num = '无'
        fea = re.findall(re_fea, html)
        if len(fea) > 0:
            fea = ' '.join(fea)
        else:
            fea = '无'
        subname = re.findall(re_subname, html)

        if len(subname) > 0:
            subname = subname[0]
        else:
            subname = '无'
        star = re.findall(re_star, html)

        # 正好跟40或45或50，其他的不是，如：40 cross-sells-items-grid-comparisons-Icon__icon--2fevQ
        if len(star) > 0 and len(star[0])<3:

            star = str(int(star[0]) / 10)

        else:
            star = '无'

        prize = re.findall(re_prize, html)
        if len(prize) > 0:
            cc = set(prize)
            prize = ' '.join(cc)
        else:
            prize = '无'

        discribe = re.findall(re_discribe, html)
        if len(discribe) > 0:
            discribe = discribe[0]
        else:
            discribe = ''
        style = re.findall(re_style, html)

        if len(style) > 0:
            bb = set(style)
            style = ' '.join(bb)
        else:
            style = '无'

        room_style = re.findall(re_room_style, html)
        if len(room_style) > 0:
            room_style = room_style[0]
        else:
            room_style = '无'
        have_website = re.findall(re_have_website, html)
        if len(have_website) > 0:

            have_website = 'have'

        else:
            have_website = 'no'

        have_email = re.findall(re_have_email, html)

        if len(have_email) > 0:

            have_email = 'have'

        else:
            have_email = 'no'
        near_name = re.findall(re_near_name, html)
        near_distance = re.findall(re_near_distance, html)
        locid = re.findall(re_locid, html)[-12:]
        comment_id = re.findall(re_comment_id, html)
        stay_hotel_date = re.findall(re_stay_hotel_date, html)
        comment_date = re.findall(re_comment_date, html)
        comment_star = re.findall(re_comment_star, html)
        comment_title = re.findall(re_comment_title, html)
        comment_context = re.findall(re_comment_context, html)
        comment_person = re.findall(re_comment_person, html)

        one_hotel = [hotel_id, name, name_en, discount, discount_net, rank, comment_count, grade, address, pic_num, fea,
                     subname, star, prize, discribe, room_style, style, have_website, have_email]

        le = min([len(comment_id),len(stay_hotel_date),len(comment_date),len(comment_person),len(comment_star),len(comment_title),len(comment_context)])
        for i in range(le):
            one_comment = [comment_id[i], hotel_id, stay_hotel_date[i], comment_date[i], comment_person[i],
                           comment_star[i], comment_title[i], comment_context[i]]
            one_hotel_comments.append(one_comment)

        xx = min([len(near_distance),len(locid),len(near_name)])  # 12
        xxx = int(xx / 3)  # 4
        xxxx = 2 * xxx  # 8

        if xx>= 3:#有的没有周边推荐
            for i in range(xxx):
                one_near_hotel.append([hotel_id, locid[i], near_name[i], near_distance[i]])
            for i in range(xxx, xxxx):
                one_near_eating.append([hotel_id, locid[i], near_name[i], near_distance[i]])
            for i in range(xxxx, xx):
                one_near_scene.append([hotel_id, locid[i], near_name[i], near_distance[i]])


        print(one_hotel,one_hotel_comments,one_near_hotel,one_near_eating,one_near_scene)
        return one_hotel,one_hotel_comments,one_near_hotel,one_near_eating,one_near_scene

    def sprider_urls(self):

        socket.setdefaulttimeout(20)
        # 每次随机获取一个代理ip和头部

        proxy ={}
        header = random.choice(self.headers)
        aa = requests.get(url='http://api3.xiguadaili.com/ip/?tid=556723315772516&num=1&delay=1&protocol=https&filter=on')
        proxy['https'] = aa.text
        aa.close()


        length = len(self.urls)
        for i in range(12641,length):
            print('\r 下标%d:长度%d' %(i,length,), end='')
            time.sleep(0.03)
            if i%400 == 0:
                aa = requests.get(url='http://api3.xiguadaili.com/ip/?tid=556723315772516&num=1&delay=1&protocol=https&filter=on')
                proxy['https'] = aa.text
                aa.close()

            url = self.urls[i]
            req = ''
            # req有返回值（requests.get连接异常时无返回值），有返回值，也可能为不是正常的页面
            while(req == ''):
                try:
                    # proxies = proxy,
                    req = requests.get(url=url, headers=header, proxies = proxy,timeout=(3,3))
                # except requests.exceptions.Timeout or requests.exceptions.ProxyError or ConnectionRefusedError or ConnectionResetError or requests.exceptions.ConnectionError or socket.timeout or urllib3.exceptions.ReadTimeoutError as e:
                except Exception as e:
                    # 更换代理池和头部
                    aa = requests.get(
                        url='http://api3.xiguadaili.com/ip/?tid=556723315772516&num=1&delay=1&protocol=https&filter=on')
                    proxy['https'] = aa.text
                    aa.close()
                    header = random.choice(self.headers)
                    print('超时，更换代理和头部',e)
                    # 无req.close()因为此时无返回req

            while(req.status_code != 200):  # 如果没有正常获得数据

                req.close()  # 关闭连接
                # time.sleep(2)
                req = ''
                # req有返回值（requests.get连接异常时无返回值），有返回值，也可能为不是正常的页面
                while (req == ''):
                    try:
                        # proxies = proxy,
                        req = requests.get(url=url, headers=header, proxies = proxy,timeout=(3,3))
                    # except requests.exceptions.Timeout or requests.exceptions.ProxyError or ConnectionRefusedError or ConnectionResetError or ConnectionRefusedError or requests.exceptions.ConnectionError or socket.timeout or urllib3.exceptions.ReadTimeoutError as e:
                    except Exception as e:
                        # 更换代理池和头部
                        aa = requests.get(url='http://api3.xiguadaili.com/ip/?tid=556723315772516&num=1&delay=1&protocol=https&filter=on')
                        proxy['https'] = aa.text
                        aa.close()
                        header = random.choice(self.headers)
                        print('超时，更换代理和头部', e)
                        # 无req.close()因为此时无返回req



            one_hotel, one_hotel_comments, one_near_hotel, one_near_eating, one_near_scene = self.get_info(req.text,url)

            req.close()

            self.hotels.append(one_hotel)
            self.comments.extend(one_hotel_comments)
            self.near_hotels.extend(one_near_hotel)
            self.near_eatings.extend(one_near_eating)
            self.near_scenes.extend(one_near_scene)

            if len(self.hotels)==100:

                with open('hotels.txt','a',encoding='utf-8') as f:
                    f.write(json.dumps(self.hotels,ensure_ascii=False)+'\n')
                with open('comments.txt', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(self.comments, ensure_ascii=False)+'\n')
                with open('near_hotels.txt', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(self.near_hotels, ensure_ascii=False)+'\n')
                with open('near_eatings.txt', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(self.near_eatings, ensure_ascii=False)+'\n')
                with open('near_scenes.txt', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(self.near_scenes, ensure_ascii=False)+'\n')

                # 清空列表
                self.hotels.clear()
                self.comments.clear()
                self.near_hotels.clear()
                self.near_eatings.clear()
                self.near_scenes.clear()

        # 把最后的不到100的数据条存入
        with open('hotels.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(self.hotels, ensure_ascii=False) + '\n')
        with open('comments.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(self.comments, ensure_ascii=False) + '\n')
        with open('near_hotels.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(self.near_hotels, ensure_ascii=False) + '\n')
        with open('near_eatings.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(self.near_eatings, ensure_ascii=False) + '\n')
        with open('near_scenes.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(self.near_scenes, ensure_ascii=False) + '\n')








if __name__ == '__main__':

        file_path_urls = r'./all_hotel_urls.txt'
        # 加载酒店链接
        urls = load_urls(file_path_urls)
        print('加载酒店链接成功')
        print(urls[0])

        # 全局变量 格式[{'http':'www.baidu.com:8080'},]
        # page_num = 20
        # proxies = get_proxies.GetProxies(page_num).get_proxies()
        # print('获取代理池成功')
        proxies = []
        with open('./ips.txt','r',encoding='utf-8') as f:
            for line in f:
                one = {}
                one['https'] = line.strip()
                proxies.append(one)
        print(proxies[0])

        # 获取头部池 [{'User-Agent': "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"},]
        headers = get_headers.GetHeaders().get_headers()
        print('获取头部s成功')
        print(headers[0])

        print('进行爬取所有的链接s..')
        sprider = Sprider(proxies,headers,urls)
        sprider.sprider_urls()






