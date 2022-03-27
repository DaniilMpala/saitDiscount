import json
import re
import time
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from pymongo import ReturnDocument
from bson.objectid import ObjectId

client = MongoClient(
    'mongodb+srv://testSait:test123Q@cluster0.obuew.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.catalog
Catalog = db["Catalog"]
Category = db["Category"]
Shops = db["ShopsName"].find_one({"title": "Лента"})


# search_this_string = "text"
# print(list(Catalog.find({"$text": {"$search": search_this_string}})))
# Это парсер магазинов с html страницы (товара) ленты


class startParser:
    def getAvailability(url):
        time.sleep(1)
        r = requests.get(url, headers={
            "user-agent": "node-fetch"
        })

        if r.status_code != 200:
            return None
        h = BeautifulSoup(r.text, 'lxml')
        retJson = {}
        # у них хранятся все магазины в атрибуте в одном блоке поэтмоу этот блок распарсиваю
        for js in json.loads(h.find_all("div", {"class": "sku-page-control-container sku-page__control"})[0]["data-model"])["storesWithSku"]:
            retJson.update({js['storeName']: js["stockBalance"]})

        return retJson

    # Это сам парсер

    def parserLenta():
        offsetLast = 0
        totalCount = 1
        # это каталоги в ленте где есть какие то товары продукты/для дома и тд
        allCat = ("gd6dd9b5e854cf23f28aa622863dd6913", "g301007c55a37d7ff8539f1f169a4b8ae", "g68552e15008531b8ae99799a1d9391df", "g7cc5c7251a3e5503dc4122139d606465", "geee7643ec01603a5db2cf4819de1a033", "g0a4c6ef96090b5b3db5f6aa0f2c20563", "g0a4c6ef96090b5b3db5f6aa0f2c20563", "gaaa3a99413aa9e3963f7f07ed7a75ec0", "g523853c00788bbb520b022c130d1ae92", "g604e486481b04594c32002c67a2b459a", "gce3c6ce98ad51e02445da35b93d2c7b7", "gd152557d86db1829c25705de4db3cf66",
                  "g4258530b46e66c5ac62f88a56ee8bce1", "ga4638d8e16b266a51b9906c290531afb", "g36505197bc9614e24d1020b3cfb38ee5", "g4477ab807af5fd53f280b1aac7816659", "g81ed6bb4ec3cd75cbf9117a7e9722a1d", "g6b6be260dbddd6da54dcc3ca020bf380", "g1d79df330af0458391dd6307863d333e", "g1baf1ddaa150137098383967c9a8e732", "g9290c81c23578165223ca2befe178b47", "g7886175ed64de08827c4fb2a9ad914f3", "ge638b7ffc736e21c16b21710b4086220", "g6f4a2d852409e5804606d640dc97a2b1", "gb57865aeafbfc5aa8e086b86d3000a27", "g648e6f3e83892dabd3f63281dab529fd")
        for cat in allCat:
            while (totalCount > offsetLast):
                # запросы делаем к ленте с разным началом offset
                print("Запрос")
                r = requests.post("https://lenta.com/api/v1/skus/list",
                                  headers={
                                      "content-type": "application/json",
                                      "user-agent": "node-fetch"
                                  },
                                  json={"nodeCode": cat, "filters": [], "typeSearch": 1,
                                        "sortingType": "ByCardPriceAsc", "offset": offsetLast, "limit": 24, "updateFilters": True},
                                  )
                print(r.status_code, totalCount, offsetLast)
                if r.status_code != 200 or r.json()["totalCount"] == 0:
                    time.sleep(1)
                    continue
                totalCount = r.json()["totalCount"]
                print("Всего ",totalCount)
                for v in r.json()["skus"]:
                    # skus - каталог товаров
                    # выделям массу если она есть из название товара
                    title = re.search("[0-9]{1,}[ ]?мл", v['title']) or re.search("[0-9]{1,}[ ]?г", v['title']
                                                                                  ) or re.search("[0-9]{1,}[ ]?кг", v['title']) or re.search("[0-9]{1,}[ ]?л", v['title'])
                    # weightOptionsMax - весовой парметр товара типо вес шашлыка хаха)
                    # valueSymbol - цена за кг/л
                    valueSymbol = v["cardPrice"]["value"] if len(
                        v["weightOptionsMax"]) > 0 and v["weightOptionsMax"] else None
                    # параметр Л или КГ
                    symbol = "кг" if len(v["weightOptionsMax"]
                                         ) > 0 and v["weightOptionsMax"] else None
                    if title:
                        decimal = float(re.search("[0-9.,]{1,}", title[0])[0])
                        symbol = re.search("[млгрМЛГРКГ]{1,}", title[0])[
                            0].lower()
                        valueSymbol = v["cardPrice"]["value"] * 1000 / \
                            decimal if symbol == "гр" or symbol == "мл" or symbol == "г" else v[
                                "cardPrice"]["value"] / decimal

                    if symbol == "мл":
                        symbol = "л"
                        decimal = decimal / 1000
                    if symbol == "г":
                        symbol = "кг"
                        decimal = decimal / 1000
                    if symbol == "гр":
                        symbol = "кг"
                        decimal = decimal / 1000

                    # составляем регулярное выражение поиска по названию в БД
                    # find = "(^|[^_0-9a-zA-Zа-яёА-ЯЁ])"
                    # for word in v["title"]:
                    #     if(word == " "):
                    #         find += "([^_0-9a-zA-Zа-яёА-ЯЁ])|"
                    #         continue

                    #     find += f"[{word}"
                    #     match word:
                    #         case "о": find += "а"
                    #     find += "]?"

                    # find += "([^_0-9a-zA-Zа-яёА-ЯЁ]|$)"

                    # allCategory = v["gaCategory"].split("/")

                    # # Проверяем какие категории у нас есть и если есть то убираем категорию из долнейшего добавления
                    # for i in range(len(allCategory)):
                    #     if Category.find_one({"title": allCategory[i]}) != None:
                    #         allCategory[i] = None
                    #     else:
                    #         allCategory[i] = {"title": allCategory[i]}
                    # allCategory = list(filter(None, allCategory))

                    # if len(allCategory) >= 1:
                    #     Category.insert_many(allCategory)


                    category = v["gaCategory"].split("/")[0]
                    if(Category.find_one({"title": category}) == None):
                        Category.insert_one({"title": category})

                    d = Catalog.find_one({"title": v["title"]})

                    infoProduct = {
                        "Shop": {
                            "img": Shops["img"],
                            "title": Shops["title"]
                        },
                        "tovar": {
                            "value": v["cardPrice"]["value"],
                            "oldValue":v["regularPrice"]['value'],
                            "valueSymbol": round(valueSymbol, 2) if valueSymbol != None else None,
                            "stockValue": v["stockValue"],
                            "promoPercent": v["promoPercent"],
                            "promoEnd": v["promoEnd"],
                            "promoStart": v["promoStart"],
                            "productUrl": "http://lenta.com" + v["skuUrl"],
                            "availabilityShop": startParser.getAvailability("http://lenta.com" + v["skuUrl"]),
                        }}

                    if d == None:
                        print("Добавляем товар")
                        Catalog.insert_one({
                            "countBuy": 0,
                            "title": v["title"],
                            "img": v["imageUrl"],
                            "category": v["gaCategory"],
                            "weight": decimal,
                            "symbol": symbol,
                            "shops": [infoProduct]
                        })
                    else:
                        print("Обновляем товар")

                        for i in range(len(d["Shop"])):
                            if d["shops"][i]["Shop"]["title"] == "Лента":
                                d["shops"][i] = infoProduct

                        d["shops"] = dict(sorted(d["shops"].items(), key=lambda x: x[0]))

                        Catalog.update_one({
                            "_id": d["_id"]
                        }, {
                            "$set": {"shops": d["shops"]}
                        })

                offsetLast += len(r.json()["skus"])

                print(totalCount, offsetLast)
