from urllib.request import urlopen
import json
import csv

url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
url_en = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

response = urlopen(url)
data = json.load(response)
hotels = data["list"]

response_en = urlopen(url_en)
data_en = json.load(response_en)
hotels_en = data_en["list"]

english_hotels = {}

for hotel in hotels_en:
    hotel_id = hotel["_id"]
    english_hotels[hotel_id] = hotel

with open("hotels.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    for hotel in hotels:
        hotel_id = hotel["_id"]

        ch_name = hotel["旅宿名稱"]
        ch_address = hotel["地址"]
        phone = hotel["電話或手機號碼"]
        room_count = hotel["房間數"]

        en_hotel = english_hotels[hotel_id]
        en_name = en_hotel["hotel name"]
        en_address = en_hotel["address"]

        writer.writerow([
            ch_name,
            en_name,
            ch_address,
            en_address,
            phone,
            room_count
        ])

district_names = [
    "中正區", "大同區", "中山區", "松山區",
    "大安區", "萬華區", "信義區", "士林區",
    "北投區", "內湖區", "南港區", "文山區"
]

districts = {}

for hotel in hotels:
    address = hotel["地址"]
    room_count = int(hotel["房間數"])

    for district_name in district_names:
        if district_name in address:
            if district_name not in districts:
                districts[district_name] = {
                    "hotel_count": 0,
                    "room_count": 0
                }

            districts[district_name]["hotel_count"] += 1
            districts[district_name]["room_count"] += room_count
            break

with open("districts.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    for district_name in districts:
        writer.writerow([
            district_name,
            districts[district_name]["hotel_count"],
            districts[district_name]["room_count"]
        ])