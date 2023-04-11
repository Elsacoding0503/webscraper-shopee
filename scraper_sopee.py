# shopee_居家生活
import requests
import pandas as pd
import time, random
import json
from fake_useragent import UserAgent 
import re

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

# 多字元清洗
symbols = ['【', '】']
product_all['product_name'] = product_all['product_name'].replace(dict.fromkeys(symbols, ''), regex=True)

# emoji 清洗
emoji_pattern = re.compile(
    "(["

    "\U0001F1E0-\U0001F1FF" # flags (iOS)

    "\U0001F300-\U0001F5FF" # symbols & pictographs

    "\U0001F600-\U0001F64F" # emoticons

    "\U0001F680-\U0001F6FF" # transport & map symbols

    "\U0001F700-\U0001F77F" # alchemical symbols

    "\U0001F780-\U0001F7FF" # Geometric Shapes Extended

    "\U0001F800-\U0001F8FF" # Supplemental Arrows-C

    "\U0001F900-\U0001F9FF" # Supplemental Symbols and Pictographs

    "\U0001FA00-\U0001FA6F" # Chess Symbols

    "\U0001FA70-\U0001FAFF" # Symbols and Pictographs Extended-A

    "\U00002702-\U000027B0" # Dingbats

    "])")

product_all['product_name'] = product_all['product_name'].str. replace(emoji_pattern, '')
product_all['reviews'] = product_all['reviews'].str. replace(emoji_pattern, '')
product_all.to_excel('shopee_clean.xlsx', sheet_name='居家生活',index=False, encoding='utf8')


product_all.to_excel('shopee_clean.xlsx', sheet_name='居家生活',index=False, encoding='utf8')
# print(product_all)
