import requests
import json
import statistics as stat

url_leagues = 'https://api.pathofexile.com/leagues'
url_currency = 'https://www.pathofexile.com/api/trade/exchange/'
url_get = 'https://www.pathofexile.com/api/trade/fetch/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212',
    'From': 'youremail@domain.com'  # This is another valid field
}

response = requests.get(url_leagues, headers=headers)
leagues = json.loads(response.text)
leagues_list = []

for i in leagues:
    leagues_list.append(i.get('id'))

for i, item in enumerate(leagues_list):
    print((i - 1) + 1, item)
print('Выберете лигу:')
choise_league = leagues_list[int(input())]
url_currency += choise_league


def get_exa_value():
    return get_currency_price("exalted")


def get_currency_price(want, have='chaos', head=10):
    myobj = {
        "exchange": {
            "want": [want],
            "have": [have],
            "status": "online"
        }
    }
    respond = requests.post(url_currency, json=myobj, headers=headers)
    respond = json.loads(respond.text)
    respond_id = respond["id"]
    # ignore first 2 listing
    respond_result = respond["result"][2:head + 2]

    myobj = ",".join(respond_result)
    url_get_item = url_get + '%s?query=%s' % (myobj, respond_id)
    respond = requests.get(url_get_item, headers=headers)
    respond = json.loads(respond.text)

    respond_result = respond["result"]
    price_catalog = []
    for x in respond_result:
        listing = x["listing"]
        price = listing["price"]
        price_catalog.append(price["amount"])
    price = round((stat.mean(price_catalog) + stat.median(price_catalog)) / 2, 4)
    return price


a = ['wisdom', 'portal', 'alt', 'alch', 'gcp', 'fusing', 'chrome', 'jewellers', 'orb-of-horizons', 'transmute', 'aug',
     'p', 'silver', 'chance', 'chisel', 'scour', 'blessed', 'regret', 'regal', 'vaal', 'orb-of-binding', 'engineers',
     'harbingers-orb', 'scrap', 'whetstone', 'bauble']
while True:

    print("""
##################################################################################################
# 0  - Свиток мудрости   1  - Свиток портала    2  - Сфера перемен      3  - Сфера алхимии       #
# 4  - Призма камнереза  5  - Сфера соединения  6  - Цветная сфера      7  - Сфера златокузнеца  #
# 8  - Сфера горизонтов  9  - Сфера превращения 10 - Сфера усиления     11 - Монета Перандусов   #
# 12 - Серебряная монета 13 - Сфера удачи       14 - Резец картографа   15 - Сфера очищения      #
# 16 - Благодатная сфера 17 - Сфера раскаяния   18 - Сфера царей        19 - Сфера ваал          #
# 20 - Сфера сплетения   21 - Сфера инженера    22 - Сфера Предвестника 23 - Деталь доспеха      #
# 24 - Точильный камень  25 - Стекольная масса                                                   #
##################################################################################################
    """)
    currency = a[int(input('Выберете вылюту: '))]
    count = float(input("Введите количество валюты: "))
    price = get_currency_price(currency)
    total = count * price
    x = count * price
    while int(x) < total:
        count = count - 1
        total = count * price
    print(f"Вы получите {int(total + price)} хаосов за {int(count + 1)}")
    print(f"~price {int(total + price)}/{int(count + 1)} chaos", sep="")
