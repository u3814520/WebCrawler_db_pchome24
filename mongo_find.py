from pymongo import MongoClient
import pprint

client = MongoClient()
db = client.pchome
coll = db.products

# coll.find_one()  # '$options':'i' 不分大小寫
name = coll.find({'name': {'$regex': '.*KYMCO.*', '$options': 'i'}})

# 價格大於七萬  # gt大於  # gte大於等於
price = coll.find({'price': {'$gte': 70000}})

# and
data = coll.find({'$and': [{'name': {'$regex': '.*七期.*'}}, {'price': {'$gte': 70000}}]})

for d in data:
    print(d['name'], d['price'])
