import mysql.connector
from mysql.connector import errorcode
import requests
import urllib.parse

keywords=str(input("請輸入搜尋關鍵字:"))
urlkeywords = urllib.parse.quote(keywords)
DB_NAME = 'PChome'

# 連線 MySQL
try:
    cnx = mysql.connector.connect(user='ting', password='123456', host='127.0.0.1',
                                  auth_plugin='mysql_native_password')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    print('MySQL 成功連線')

cursor = cnx.cursor()


# 建立資料庫
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

# 建立TABLE  # AUTO_INCREMENT 自動遞增
TABLES = {}
TABLES['product'] = (
    "CREATE TABLE `product` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(100) NOT NULL,"
    "  `price` int NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


# 新增資料
add_product = ("INSERT INTO product "
               "(name, price) "
               "VALUES (%s, %s)")

r = requests.get(f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={urlkeywords}&page={1}&sort=sale/dc')
if r.status_code == requests.codes.ok:
    data = r.json()
    all_page = data['totalPage']
    for page in range(1,all_page+1):
        r = requests.get(f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={urlkeywords}&page={page}&sort=sale/dc')
        data = r.json()
        for product in data['prods']:
            name = product['name']
            price = product['price']
            print(f'商品名稱：{name}\n售價：{price}元')
            data_product=(name,price)
            # Insert new product (框架,data)
            cursor.execute(add_product,data_product)
            id = cursor.lastrowid   # id從最後一號接續
cnx.commit()
print('close')
cursor.close()
cnx.close()
