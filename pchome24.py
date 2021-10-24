import requests
import urllib.parse

keywords=str(input("請輸入搜尋關鍵字:"))
urlkeywords = urllib.parse.quote(keywords)


r = requests.get(f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={urlkeywords}&page={1}&sort=sale/dc')
if r.status_code == requests.codes.ok:
    data = r.json()
    # pprint.pprint(data)
    all_page = data['totalPage']
    for page in range(1,all_page+1):
        r = requests.get(f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={urlkeywords}&page={page}&sort=sale/dc')
        data = r.json()
        for product in data['prods']:
            name = product['name']
            price = product['price']
            print(f'商品名稱：{name}\n售價：{price}元')


