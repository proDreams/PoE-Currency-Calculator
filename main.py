import requests
import json
import statistics as stat

url_leagues = 'https://api.pathofexile.com/leagues'
url_currency = 'https://www.pathofexile.com/api/trade/exchange/'
url_get = 'https://www.pathofexile.com/api/trade/fetch/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212',
    'From': 'youremail@domain.com'
}


def get_leagues():
    response = requests.get(url_leagues, headers=headers)
    leagues = json.loads(response.text)
    leagues_list = []

    for i in leagues:
        leagues_list.append(i.get('id'))

    leagues_list = leagues_list[0:2] + leagues_list[4:6]

    for i, item in enumerate(leagues_list):
        print(i, item)
    choice_league = leagues_list[int(input('Выберете лигу: '))]
    global url_currency
    url_currency += choice_league


def get_currency_price(want, have='chaos'):
    price_catalog = []
    myobj = {
        "exchange": {
            "want": [want],
            "have": [have],
            "status": "online"
        },
        "engine": "new"
    }
    respond = requests.post(url_currency, json=myobj, headers=headers)
    respond = json.loads(respond.text)
    counter = 0
    for dd in respond["result"]:
        chaos = (respond['result'][dd]['listing']['offers'][0]['exchange']['amount'])
        curr = (respond['result'][dd]['listing']['offers'][0]['item']['amount'])
        price_catalog.append(chaos / curr)
        counter += 1
        if counter == 15:
            break

    total_price = round((stat.mean(price_catalog[2:]) + stat.median(price_catalog[2:])) / 2, 4)

    return total_price


currencies_list = ['wisdom', 'portal', 'alt', 'alch', 'gcp', 'fusing', 'chrome', 'jewellers', 'orb-of-horizons', 'transmute', 'aug',
     'orb-of-unmaking', 'rogues-marker', 'chance', 'chisel', 'scour', 'blessed', 'regret', 'regal', 'vaal', 'orb-of-binding', 'engineers',
     'harbingers-orb', 'scrap', 'whetstone', 'bauble', 'splinter-xoph', 'splinter-tul', 'splinter-esh', 'splinter-uul', 'splinter-chayula',
     'simulacrum-splinter', 'dusk', 'mid', 'dawn', 'noon', 'offer', 'divine-vessel']

get_leagues()

while True:

    print("""
###################################################################################################
# Валюта                                                                                          #
# 0  - Свиток мудрости    1  - Свиток портала    2  - Сфера перемен      3  - Сфера алхимии       #
# 4  - Призма камнереза   5  - Сфера соединения  6  - Цветная сфера      7  - Сфера златокузнеца  #
# 8  - Сфера горизонтов   9  - Сфера превращения 10 - Сфера усиления     11 - Сфера небытия       #
# 12 - Разбойничий жетон  13 - Сфера удачи       14 - Резец картографа   15 - Сфера очищения      #
# 16 - Благодатная сфера  17 - Сфера раскаяния   18 - Сфера царей        19 - Сфера ваал          #
# 20 - Сфера сплетения    21 - Сфера инженера    22 - Сфера Предвестника 23 - Деталь доспеха      #
# 24 - Точильный камень   25 - Стекольная масса                                                   #
# Фрагменты, осколки, прочее                                                                      #
# 26 - Осколок Ксофа      27 - Осколок Тул       28 - Осколок Иш         29 - Осколок Уул-Нетол   #
# 30 - Осколок Чаюлы      31 - Осколок Симулякра 32 - Жертва на закате   33 - Жертва в полночь    #
# 34 - Жертва на рассвете 35 - Жертва в полдень  36 - Подношение богине  37 - Божественный сосуд  #
###################################################################################################
    """)
    currency = currencies_list[int(input('Выберете вылюту: '))]
    count = float(input("Введите количество валюты: "))
    price = get_currency_price(currency)
    total = count * price
    x = count * price
    while int(x) < total:
        count = count - 1
        total = count * price
    print(f"Вы получите {int(total + price)} хаосов за {int(count + 1)}")
    print(f"~price {int(total + price)}/{int(count + 1)} chaos", sep="")
