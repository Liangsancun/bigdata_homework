import time
import json
import requests
import re
all_city_url={}
wrong=[]
for prov,cities in all_city.items():
    one_city_url=[]
    for city in cities:
        print('\r %s:%s'%(prov,city),end='')
        url='https://www.tripadvisor.cn/TypeAheadJson?&types=geo&matchKeywords=true&parentids=294211&query='+city+'&action=API'
        try:
            req=requests.get(url)
        except Exception as e:
            wrong.append(prov+':'+city)
            continue
        else:
            reqq=json.loads(req.text)
            one_url='https://www.tripadvisor.cn'+reqq['results'][0]['url']
            one_city_url.append(one_url)
        req.close()
        time.sleep(0.2)
    all_city_url[prov]=one_city_url
    
for value in all_city_url.values():
    for i in value:
        city_urls.append(i)

city_infoes=[]
index_length=len(temp)-1
for i, url in enumerate(temp):
    print('\r 下标 %d:%d'%(i,index_length),end='')
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.33 Safari/537.36'}
    req=requests.get(url,headers=head,timeout=(5,3))
    re_city=r'class="breadcrumb">(.+?)</li>'
    re_prov=r'itemprop="title">(.+?)</span>'
    re_hotel_count=r'class="typeQty">(.+?)</span>'
    re_comment_count=r'class="contentCount">(.+?)</span>'
    re_hotels=r'a href="(.+?)" data-trk="hotels_nav"'
    bianhao=url.split('-')[1]
    html=req.text
    
    city=re.findall(re_city,html)[0][:-2]
    prov=re.findall(re_prov,html)[-1]
    if prov == '中国':
        prov=city
    hotel_count=re.findall(re_hotel_count,html)[0].strip('()')
    comment_count=re.findall(re_comment_count,html)[0][:-3]
    hotel_urls='https://www.tripadvisor.cn'+re.findall(re_hotels,html)[0]
    
    city_infoes.append([bianhao,city,prov,hotel_count,comment_count,hotel_urls])
    
    req.close()
    temp.remove(url)
    if i%20==0:
        time.sleep(3)
    else:
        time.sleep(0.5)

all_all_hotel_urls=[]
all_hotel_urls=[]
for i in city_infoes:
    all_all_hotel_urls.append(i[-1])

all_all_hotel_urls_info=[]
index_length=len(all_all_hotel_urls)-1
for i,url in enumerate(all_all_hotel_urls):
    print('\r 下标%d:%d:%s'%(i,index_length,url),end='')
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.33 Safari/537.36'}
    proxies={'http':'140.207.50.246:51426'}
    req = requests.get(url, headers=head, proxies=proxies,timeout=(10))
   
    html=req.text
    req.close()
    if i%10==0:
        time.sleep(2)
    else:
        time.sleep(0.03)
    re_page_num=r'data-page-number="(.+?)"'
    re_pre_page=r'class="nav previous ui_button secondary disabled">(.+?)</span>'
    page_num=re.findall(re_page_num,html)
    pre_page=re.findall(re_pre_page,t)
#      print(page_num)

    #有上一页（不是只有一页url），
    if len(page_num)>0 and len(pre_page)>0:
        max_page_num=page_num[-1]
    else:
        max_page_num=1
    all_all_hotel_urls_info.append([url,1,max_page_num])
    all_all_hotel_urls.remove(url)

index_length=len(all_all_hotel_urls_info)-1
for i,info in enumerate(all_all_hotel_urls_info):
   
   
    if len(all_all_hotel_urls_info)>0:
        url=info[0]
        now_page=info[1]
        max_page=info[2]
        
        while(now_page<=max_page):
            
            a=url.split('-')
            b=[a[0],a[1],'oa'+str(30*(now_page_num-1)),a[2],a[3]]
            new_url='-'.join(b)
            
            
            head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.33 Safari/537.36'}
            proxies={'http':'140.207.50.246:51426'}
            req = requests.get(new_url, headers=head, proxies=proxies,timeout=(10))

            html=req.text
            req.close()
            if i%10==0:
                time.sleep(​index_length=len(all_all_hotel_urls_info)-1

for i,info in enumerate(all_all_hotel_urls_info):
   
   
    if len(all_all_hotel_urls_info)>0:
        url=info[0]
        now_page=info[1]
        max_page=info[2]
        
        while(now_page<=max_page):
            
            a=url.split('-')
            b=[a[0],a[1],'oa'+str(30*(now_page_num-1)),a[2],a[3]]
            new_url='-'.join(b)
            
            
            head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.33 Safari/537.36'}
            proxies={'http':'140.207.50.246:51426'}
            req = requests.get(new_url, headers=head, proxies=proxies,timeout=(10))

            html=req.text
            req.close()
            if i%10==0:
                time.sleep(3)
            else:
                time.sleep(0.3)
                
            
            re_hotel_urls=r'target="_blank" href="(.+?)" id='
            hotel_urls=re.findall(re_hotel_urls,html)   
            all_hotel_urls.extend(hotel_urls)
            
            print('\r 下标%d:%d:%d:%d'%(i,index_length,now_page,max_page),end='')
            #页数加一
            all_all_hotel_urls_info[i][1]=now_page+1
            now_page=info[1]
       
        all_all_hotel_urls_info.remove(info)3)
            else:
                time.sleep(0.3)
                
            
            re_hotel_urls=r'target="_blank" href="(.+?)" id='
            hotel_urls=re.findall(re_hotel_urls,html)   
            all_hotel_urls.extend(hotel_urls)
            
            print('\r 下标%d:%d:%d:%d'%(i,index_length,now_page,max_page),end='')
            #页数加一
            all_all_hotel_urls_info[i][1]=now_page+1
            now_page=info[1]
       
        all_all_hotel_urls_info.remove(info)

html_arr=[]
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.33 Safari/537.36'}
proxies={'http':'171.41.81.27:9999'}
n=0
length=len(all_hotel_urls)
while(length>0):
    n=n+1
    url='https://www.tripadvisor.cn'+all_hotel_urls[-1]
    print('\r %d'%(length,),end='')
   
    req = requests.get(url, headers=head, proxies=proxies,timeout=(10))
   
    html=req.text
    req.close()
    if n%300==0:
        time.sleep(1)
    time.sleep(0.03)
    
    html_arr.append(html)
    
    all_hotel_urls.pop()
    length=len(all_hotel_urls)


hotels=[]
comments=[]
comment_man_url=[]#[]
near_hotels=[]
near_eating=[]
near_scene=[]



one_near_hotel=[]
one_near_eating=[]
one_near_scene=[]

length=len(html_arr)
while(length>0):
    
    html=html_arr[-1]
    re_name=r'<h1 id="HEADING"class="ui_header h1">(.+?)<div' 
    re_name_en=r'class="is-hidden-mobile">(.+?)</div>'
    re_discount=r'data-sizegroup="hr_chevron_prices">￥(.+?)</div>'
    re_discount_2=r'<div class="bb_price_text ">￥(.+?)</div>'
    re_discount_net=r'class="providerImg"  alt="(.+?)" />'
    re_rank=r'class="rank">(.+?)</b>'
    re_comment_count=r'class="reviewCount ">(.+?) 条点评</span>'
    re_grade=r'class="ui_bubble_rating bubble_(.+?)" style='
    re_address_1=r'<span class="detail ">(.+?)<span class="locality"'
    re_address_2=r'class="locality">(.+?)</span>'
    re_address_3=r'<span class="street-address">(.+?)</span>'
    re_address_4=r'class="postal-code">(.+?)</span></span>'

    re_pic_num=r'class="is-hidden-mobile hotels-media-album-parts-PhotoCount__text--3OXuH">(.+?)</span>'
    re_fea=r'class="entry ui_column is-4-tablet is-6-mobile is-4-desktop"><DIV class="textitem" data-prwidget-name="text" data-prwidget-init="">(.+?)</DIV'
    re_subname=r'<div class="sub_title">别名</div><div class="sub_content"><DIV class="textitem" data-prwidget-name="text" data-prwidget-init="">(.+?)</DIV>'
    re_star=r'class="ui_star_rating star_(.+?)"'
    re_prize=r'class="ui_icon certificate-of-excellence">(.+?)</'
    re_discribe=r'class="introText">(.+?)<span class="seeMore"'
    re_style=r'<DIV class="textitem style" data-prwidget-name="text" data-prwidget-init="">(.+?)</DIV>'
    re_room_style=r'class="sub_title">客房类型</div><div class="sub_content"><DIV class="textitem" data-prwidget-name="text" data-prwidget-init="">(.+?)</DIV>'
    re_have_website=r'class="detail blue_test">(.+?)</span>'
    re_have_email=r'span class="detail">联系酒店</(.+?)>'
    re_near_name=r'class="poiName" dir="auto">(.+?)</'
    re_near_distance=r'class="distance">(.+?)</'
    re_locid=r'data-locid="(.+?)"'
    re_comment_id=r';"id="(.+?)"><span class=\'noQuotes\'>'
    re_stay_hotel_date=r'<span class="stay_date_label">入住日期：</span>(.+?)</DIV>'
    re_comment_date=r'<span class="ratingDate" title=\'(.+?)\' '
    re_comment_title=r'span class=\'noQuotes\'>(.+?)</span>'
    re_comment_context=r'<p class="partial_entry" >(.+?)</p>'
    re_comment_star=r'<div class="ui_column is-9"><span class="ui_bubble_rating bubble_(.+?)'
    re_comment_person=r';"><div>(.+?)</div>'
    
    hotel_id=url.split('-')[2]
    name=re.findall(re_name,html)[0]
    name_en=re.findall(re_name_en,html)[0]

    discount_1=re.findall(re_discount,html)

    if len(discount_1)>0:
        discount_1=discount_1[0]
    else:
        discount_1=''
    discount_2=re.findall(re_discount_2,html)
    if len(discount_2)>0:
        discount_2=discount_2[0]
    else:
        discount_2=''
    discount=discount_1+discount_2

    discount_net=re.findall(re_discount_net,html)

    if len(discount_net)>0:
        discount_net=discount_net[0]


    else:
        discount_net='无'
    rank=re.findall(re_rank,html)

    if len(rank)>0:
        rank=rank[0][3:]
    else:
        rank='无'
    comment_count=re.findall(re_comment_count,html)
    if len(comment_count)>0:
        comment_count=comment_count[0]
    else:
        comment_count='无'

    grade=re.findall(re_grade,html)
    if len(grade)>0:
        grade=str(int(grade[0])/10)
    else:
        grade='无'

    address_1=re.findall(re_address_1,html)
    if len(address_1)>0:
        a=address_1[0]
        if len(a)>10:
            address_1=''
        else:
            address_1=a
    else:
        address_1=''
    address_2=re.findall(re_address_2,html)[0]
    address_3=re.findall(re_address_3,html)[0]
    address_4=re.findall(re_address_4,html)
    if len(address_4)==0:
        address_4=''
    else:
        address_4=address_4[0]
    address=address_1+address_2+address_3+address_4

    pic_num=re.findall(re_pic_num,html)

    if len(pic_num)>0:
        pic_num=pic_num[0].split('>')[2].split('<')[0]
    else:
        pic_num='无'
    fea=re.findall(re_fea,html)
    if len(fea)>0:
        fea=' '.join(fea)
    else:
        fea='无'
    subname=re.findall(re_subname,html)

    if len(subname)>0:
        subname=subname[0]
    else:
        subname='无'
    star=re.findall(re_star,html)
    print(star)
    if len(star)>0:

        star=str(int(int(star[0])/10))

    else:
        star='无'

    prize=re.findall(re_prize,html)
    if len(prize)>0:
        cc=set(prize)
        prize=' '.join(cc)
    else:
        prize='无'

    discribe=re.findall(re_discribe,html)
    if len(discribe)>0:
        discribe=discribe[0]
    else:
        discribe=''
    style=re.findall(re_style,html)

    if len(style)>0:
        bb=set(style)
        style=' '.join(bb)
    else:
        style='无'

    room_style=re.findall(re_room_style,html)
    if len(room_style)>0:
        room_style=room_style[0]
    else:
        room_style='无'
    have_website=re.findall(re_have_website,html)
    if len(have_website)>0:

        have_website='have'

    else:
        have_website='no'

    have_email=re.findall(re_have_email,html)

    if len(have_email)>0:

        have_email='have'

    else:
        have_email='no'
    near_name=re.findall(re_near_name,html)
    near_distance=re.findall(re_near_distance,html)
    locid=re.findall(re_locid,html)[-12:]
    comment_id=re.findall(re_comment_id,html)
    stay_hotel_date=re.findall(re_stay_hotel_date,html)
    comment_date=re.findall(re_comment_date,html)
    comment_star=re.findall(re_comment_star,html)
    comment_title=re.findall(re_comment_title,html)
    comment_context=re.findall(re_comment_context,html)
    comment_person=re.findall(re_comment_person,html)
    
    one_hotel=[hotel_id,name,name_en,discount,discount_net,rank,comment_count,grade,address,pic_num,fea,subname,star,prize,discribe,room_style,style,have_website,have_email]
    hotels.append(one_hotel)
    
    for i in range(5):
        one_comment=[comment_id[i],hotel_id,stay_hotel_date[i],commend_date[i],comment_person[i],comment_star[i],comment_title[i],comment_context[i]]
        comments.append(one_comment)
    for i in range(4):
        one_near_hotel.append([hotel_id,locid[i],near_name[i],near_distance[i]])
    for i in range(4,8):
        one_near_eating.append([hotel_id,locid[i],near_name[i],near_distance[i]])
    for i in range(8,12):
        one_near_scene.append([hotel_id,locid[i],near_name[i],near_distance[i]])
    
    near_hotels.extend(one_near_hotel)
    near_eating.extend(one_near_eating)
    near_scene.extend(one_near_scene)

    html_arr.pop()
    length = length-1