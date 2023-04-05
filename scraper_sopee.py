import requests
import pandas as pd
import time
import json
from fake_useragent import UserAgent 

dict_of_products={}
name = []
price_min = []
price_max = []

for page in (0,60,120):
    url_shopee = f'https://shopee.tw/api/v4/recommend/recommend?bundle=category_landing_page&cat_level=1&catid=11040925&limit=60&offset={page}'
    response_shopee = requests.get(url=url_shopee)
    products = response_shopee.json()

    for i in products['data']['sections'][0]['data']['item']:
        name.append(i['name'])
        price_min.append(i['price_min']/100000)
        price_max.append(i['price_max']/100000)
    time.sleep(2)

dict_of_products['name']=name
dict_of_products['price_min']=price_min
dict_of_products['price_max']=price_max

product_all = pd.DataFrame(dict_of_products)
print(product_all)
    