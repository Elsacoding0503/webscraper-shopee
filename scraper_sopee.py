# shopee_居家生活
import requests
import pandas as pd
import time, random
import json
from fake_useragent import UserAgent 

product_reviews = []

for page in (0,60,120):
    url_shopee = f'https://shopee.tw/api/v4/recommend/recommend?bundle=category_landing_page&cat_level=1&catid=11040925&limit=60&offset={page}'
    response_shopee = requests.get(url=url_shopee)
    products = response_shopee.json()

    for i in products['data']['sections'][0]['data']['item']:
        itemid = i['itemid']
        shopid = i['shopid']
        #爬六筆評價
        sub_response = requests.get(f'https://shopee.tw/api/v2/item/get_ratings?filter=0&flag=1&itemid={itemid}&limit=6&offset=0&shopid={shopid}&type=0')        
        reviews = sub_response.json()
        
        for review in reviews['data']['ratings']:
            product_reviews.append((i['name'], i['price_min']/100000, i['price_max']/100000, review['comment']))
        time.sleep(random.uniform(1,2))
    time.sleep(random.uniform(1,3))

product_all = pd.DataFrame(product_reviews, columns=['product_name', 'price_min','price_max','reviews'])
product_all.to_excel('shopee.xlsx', sheet_name='居家生活',index=False, encoding='utf8')
# print(product_all)
