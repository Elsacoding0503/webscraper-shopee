# shopee_居家生活
import requests
import pandas as pd
import time
from bs4 import  BeautifulSoup as bs
import json
from fake_useragent import UserAgent 

dict_of_products={}
name = []
price_min = []
price_max = []
product_reviews = []

for page in (0,60,120):
    url_shopee = f'https://shopee.tw/api/v4/recommend/recommend?bundle=category_landing_page&cat_level=1&catid=11040925&limit=60&offset={page}'
    response_shopee = requests.get(url=url_shopee)
    products = response_shopee.json()

    for i in products['data']['sections'][0]['data']['item']:
        name.append(i['name'])
        price_min.append(i['price_min']/100000)
        price_max.append(i['price_max']/100000)
        itemid = i['itemid']
        shopid = i['shopid']
        sub_response = requests.get(f'https://shopee.tw/api/v2/item/get_ratings?filter=0&flag=1&itemid={itemid}&limit=6&offset=0&shopid={shopid}&type=0')        
        reviews = sub_response.json()
        
        list_of_reviews=[]
        for review in reviews['data']['ratings']:
            list_of_reviews.append(review['comment'])
        product_reviews.append(list_of_reviews)
        time.sleep(random.uniform(1,4))
    time.sleep(random.uniform(3,5))
        
        
        
dict_of_products['name']=name
dict_of_products['price_min']=price_min
dict_of_products['price_max']=price_max
dict_of_products['reviews']=product_reviews


product_all = pd.DataFrame(dict_of_products)
product_all.to_excel('shopee.xlsx', sheet_name='居家生活',index=False, encoding='utf8')
