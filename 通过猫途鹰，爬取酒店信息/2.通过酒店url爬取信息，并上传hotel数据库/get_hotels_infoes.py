import my_db
import random
import requests
import json
import re
import time
import socket

def load_urls(file_path):
    # 返回酒店链接s
    all_hotel_urls = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            all_hotel_urls.append(line.strip())
    return all_hotel_urls

class Spider(object):
    def __init__(self,xici_orderId,urls,outfile_pathes,one_save_num):
        self.headers = [{'User-Agent': 'Baiduspider+(+http://www.baidu.com/search/spider.html)'},
                        {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'},
                        {'User-Agent': 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)'},
                        {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'},
                        {'User-Agent': 'Mozilla/5.0 (compatible; Yahoo! Slurp China; http://misc.yahoo.com.cn/help.html)'},
                        {'User-Agent': "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)"},
                        {'User-Agent': "iaskspider/2.0(+http://iask.com/help/help_index.html)"},
                        {'User-Agent': "Mozilla/5.0 (compatible; iaskspider/1.0; MSIE 6.0)"},
                        {'User-Agent': "Sogou web spider/3.0(+http://www.sogou.com/docs/help/webmasters.htm#07)"},
                        {'User-Agent': "Sogou Push Spider/3.0(+http://www.sogou.com/docs/help/webmasters.htm#07)"},
                        ]
        self.xici_orderId = xici_orderId
        self.outfile_pathes = outfile_pathes
        self.urls = urls
        self.one_save_num = one_save_num

        self.hotels = []
        self.comments = []
        self.near_hotels = []
        self.near_eatings = []
        self.near_scenes = []

        self.spider_urls()


    def get_info(self,html,url):
        one_hotel = []
        one_hotel_comments = []

        one_hotel_near_hotels = []
        one_hotel_near_eatings = []
        one_hotel_near_scenes = []


        # 规则
        re_name = r'<h1 id="HEADING"class="ui_header h1">(.+?)<div'
        re_name_en = r'class="is-hidden-mobile">(.+?)</div>'
        re_discount = r'data-sizegroup="hr_chevron_prices">￥(.+?)</div>'
        re_discount_2 = r'<div class="bb_price_text ">￥(.+?)</div>'
        re_discount_net = r'class="providerImg"  alt="(.+?)" />'
        re_rank = r'class="rank">(.+?)</b>'
        re_comment_count = r'class="reviewCount ">(.+?) 条点评</span>'
        re_grade = r'class="ui_bubble_rating bubble_(.+?)" style='
        re_address_1 = r'<span class="detail ">(.+?)<span class="locality"'
        re_address_2 = r'class="locality">(.+?)</span>'
        re_address_3 = r'<span class="street-address">(.+?)</span>'
        re_address_4 = r'class="postal-code">(.+?)</span></span>'
        re_discount_2 = r'<div class="bb_price_text ">￥(.+?)</div>'
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
        re_comment_count_2 = r'class="reviewCount ui_link level_4">(.+?) 条点评</span>'


        hotel_id = url.split('-')[2]
        name = re.findall(re_name, html)
        #因为返回是个列表
        if len(name)>0:
            name =name[0]
        else:
            name = ''
        name_en = re.findall(re_name_en, html)
        if len(name_en)>0:
            name_en = name_en[0]
        else:
            name_en = ''
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
        address_2 = re.findall(re_address_2, html)
        if len(address_2)>0:
            address_2=address_2[0]
        else:
            address_2=''
        address_3 = re.findall(re_address_3, html)
        if len(address_3)>0:
            address_3=address_3[0]
        else:
            address_3=''
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

        if len(star) > 0 and len(star[0])<3:

            star = str(int(int(star[0]) / 10))

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
        #因为one_hotel=[]起初
        one_hotel.extend([hotel_id, name, name_en, discount, discount_net, rank, comment_count, grade, address, pic_num, fea,
                     subname, star, prize, discribe, room_style, style, have_website, have_email])

        le = min([len(comment_id),len(stay_hotel_date),len(comment_date),len(comment_person),len(comment_star),len(comment_title),len(comment_context)])
        for i in range(le):
            one_comment = [comment_id[i], hotel_id, stay_hotel_date[i], comment_date[i], comment_person[i],
                           comment_star[i], comment_title[i], comment_context[i]]
            one_hotel_comments.append(one_comment)

        xx = min([len(near_distance),len(locid),len(near_name)])  # 12

        xxx = int(xx / 3)  # 4
        xxxx = 2 * xxx  # 8

        if xx>= 3:#有搞头
            for i in range(xxx):
                one_hotel_near_hotels.append([hotel_id, locid[i], near_name[i], near_distance[i]])
            for i in range(xxx, xxxx):
                one_hotel_near_eatings.append([hotel_id, locid[i], near_name[i], near_distance[i]])
            for i in range(xxxx, xx):
                one_hotel_near_scenes.append([hotel_id, locid[i], near_name[i], near_distance[i]])


        print(one_hotel,one_hotel_comments,one_hotel_near_hotels,one_hotel_near_eatings,one_hotel_near_scenes)
        return one_hotel,one_hotel_comments,one_hotel_near_hotels,one_hotel_near_eatings,one_hotel_near_scenes
    def change_proxy_header(self):
        header = random.choice(self.headers)
        proxy ={}
        aa = requests.get(url='http://api3.xiguadaili.com/ip/?tid='+str(self.xici_orderId)+'&num=1&delay=1&protocol=https&filter=on')
        aa.close()
        proxy['https'] = aa.text

        self.db = my_db.DB('62.234.53.229', 'hotel', 'liang', 'liang')

        return proxy,header

    def save_one_time(self,*arrs):
        # 以存数据库的一条为一行（即一个一维数组为一行）
        #元组 接收传入的多个数组，要保存到多个文件中
        for i in range(len(arrs)):
            arr = arrs[i] #传入的第i+1个数组
            outfile_path = self.outfile_pathes[i]#对应的该数组要存入的文件名
            table_name = outfile_path.split('.txt')[0] # 'hotels.txt'->'hotels'
            print(table_name)
           # 插入数据库时，我希望收到的是一个二维数组，一个是一个数据库中的条目
            #如果该数组是二维数组
            if isinstance(arr[0],list):# arr[0]是list
                # 插入数据库
                if len(arr)==1: #如果二维数组中只有一个元素
                    arr = arr[0] #
                    # 存入数据库相应表中 #插入时，executemany(sql,[[1,2]])，[[1,2]]会被认为是只有一个参数，而不是两个参数
                                                                        #[[1,2],]或[1,2]解决
                    self.db.insert_to_table(table_name, arr, 1)
                else:
                    self.db.insert_to_table(table_name, arr, self.one_save_num)
                # 保存
                with open(outfile_path, 'a', encoding='utf-8') as f:
                    for one in arr:
                        #一个一维数组为一行
                        f.write(json.dumps(one,ensure_ascii=False)+'\n')
            # 如果该数组是一维数组，不插入数据库的，一个元素是一行
            else:
                final = ''
                with open(self.outfile_path, 'a', encoding='utf-8') as f:
                    for one in arr:
                        final += one+'\n'
                    f.write(final)



    def get_clear(self,*arrs):
        for i in arrs:
            i.clear()

    def spider_urls(self):

        # 每次随机获取一个代理ip和头部
        proxy, header = self.change_proxy_header()

        length = len(self.urls)
        for i in range(length):
            print('\r 下标%d:长度%d' %(i,length,), end='')
            time.sleep(0.3)
            if i%300 == 0:
                # 更换代理池和头部
                proxy, header = self.change_proxy_header()

            url = self.urls[i]
            req = ''
            # req有返回值（requests.get连接异常时无返回值），有返回值，也可能为不是正常的页面
            while(req == ''):
                try:

                    req = requests.get(url=url, headers=header, proxies = proxy,timeout=(3,3))
                # except requests.exceptions.Timeout or requests.exceptions.ProxyError or ConnectionRefusedError or ConnectionResetError or requests.exceptions.ConnectionError or socket.timeout or urllib3.exceptions.ReadTimeoutError as e:
                except Exception as e:
                    # print(repr(one args))可将'\n'打印出
                    print('超时，更换代理和头部', e, repr(url),repr(header),repr(proxy))
                    # 更换代理池和头部
                    proxy, header = self.change_proxy_header()

                    time.sleep(0.5)
                    # 无req.close()因为此时无返回req

            while(req.status_code != 200):  # 如果没有正常获得数据

                req.close()  # 关闭连接

                req = ''
                # req有返回值（requests.get连接异常时无返回值），有返回值，也可能为不是正常的页面
                while (req == ''):
                    try:

                        req = requests.get(url=url, headers=header, proxies = proxy,timeout=(3,3))
                    # except requests.exceptions.Timeout or requests.exceptions.ProxyError or ConnectionRefusedError or ConnectionResetError or ConnectionRefusedError or requests.exceptions.ConnectionError or socket.timeout or urllib3.exceptions.ReadTimeoutError as e:
                    except Exception as e:
                        # print(repr(one args))可将'\n'打印出
                        print('超时，更换代理和头部', e, repr(url), repr(header), repr(proxy))
                        # 更换代理池和头部
                        proxy, header = self.change_proxy_header()

                        time.sleep(0.5)
                        # 无req.close()因为此时无返回req
            req.close()

            one_hotel, one_hotel_comments, one_hotel_near_hotels, one_hotel_near_eatings, one_hotel_near_scenes = self.get_info(req.text,url)

            self.hotels.append(one_hotel)
            self.comments.extend(one_hotel_comments)
            self.near_hotels.extend(one_hotel_near_hotels)
            self.near_eatings.extend(one_hotel_near_eatings)
            self.near_scenes.extend(one_hotel_near_scenes)


            if len(self.hotels) >= self.one_save_num or i == length - 1:
                # 存储超过100条时或是最后一个连接（不超过100条）存一次
                self.save_one_time(self.hotels,self.comments,self.near_hotels,self.near_eatings,self.near_scenes)
                #清空
                self.get_clear(self.hotels,self.comments,self.near_hotels,self.near_eatings,self.near_scenes)

        # 关闭数据库连接
        self.db.close()



if __name__ == '__main__':

        file_path_urls = r'./hotel_urls.txt'
        # 加载酒店链接
        all_hotel_urls = load_urls(file_path_urls)
        print(len(all_hotel_urls))


        print('进行爬取所有的链接s..')
        xici_orderId = 556723315772516
        outfile_pathes = ['hotels.txt','comments.txt','near_hotels.txt','near_eatings.txt','near_scenes.txt']
	# 爬取酒店的信息，并上传hotel数据库
        # 获取代理的订单号，酒店urls，保存文件名，one_save_time
        Spider(xici_orderId,all_hotel_urls,outfile_pathes,100)









