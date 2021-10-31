from pymongo import MongoClient
import pprint

client = MongoClient()
db = client.pchome
coll = db.products

# coll.find_one()  # '$options':'i' 不分大小寫
name = coll.find({'name': {'$regex': '.*KYMCO.*', '$options': 'i'}})

# 價格大於七萬  # gt大於  # gte大於等於
price = coll.find({'price': {'$gte': 90000}})

# and
data = coll.find({'$and': [{'name': {'$regex': '.*七期.*'}}, {'price': {'$gte': 70000}}]})

# update
coll.update_one({'name':'光陽GP 125-鼓煞'},{'$set':{'price':56000}})

# upsert=True 如果沒有就新增
coll.update_one({'name':'Hwaiwei'},{'$set':{'price':90000,'author':'Ann'}},upsert=True)

# delete
coll.delete_one({'name':'Hwaiwei'})

for d in data:
    print(d['name'], d['price'])
