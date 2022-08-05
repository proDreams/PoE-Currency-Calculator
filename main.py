import requests
import json
import statistics as stat
import pickle

url_leagues = 'https://api.pathofexile.com/leagues'
url_currency = 'https://www.pathofexile.com/api/trade/exchange/'
url_get = 'https://www.pathofexile.com/api/trade/fetch/'
db_url = 'https://github.com/proDreams/PoE-Trade-About-Parser/raw/master/bd.pkl'
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


get_leagues()

db_file = requests.get(db_url)
with open("bd.pkl", "wb") as code:
    code.write(db_file.content)

with open('bd.pkl', 'rb') as f:
    loaded_dict = pickle.load(f)


def get_list(dic, msg):
    temp_list = []

    for i, item in enumerate(dic):
        temp_list.append(item)
        print(i, item)
    return temp_list[int(input(msg))]


while True:
    category = get_list(loaded_dict, 'Выберите категорию')
    item = get_list(loaded_dict[category], 'Выберите валюту')
    currency = loaded_dict[category][item]
    count = float(input("Введите количество валюты: "))
    price = get_currency_price(currency)
    total = count * price
    x = count * price
    while int(x) < total:
        count = count - 1
        total = count * price
    print(f"Вы получите {int(total + price)} хаосов за {int(count + 1)}")
    print(f"~price {int(total + price)}/{int(count + 1)} chaos", sep="")
