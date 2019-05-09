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




