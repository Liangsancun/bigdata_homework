import json
import time
import requests
import re

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