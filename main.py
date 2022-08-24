import requests
import json
import statistics as stat
import pickle

url_leagues = 'https://api.pathofexile.com/leagues'
url_currency = 'https://www.pathofexile.com/api/trade/exchange/'
url_get = 'https://www.pathofexile.com/api/trade/fetch/'
db_url = {
    'ru': 'https://github.com/proDreams/PoE-Trade-About-Parser/raw/master/bd_ru.pkl',
    'en': 'https://github.com/proDreams/PoE-Trade-About-Parser/raw/master/bd_en.pkl'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212',
    'From': 'youremail@domain.com'
}


def get_lang():
    languages = ['ru', 'en']
    return languages[int(input('''0 Русский
1 English
Выберите язык / Choise language: '''))]


def get_leagues():
    response = requests.get(url_leagues, headers=headers)
    leagues = json.loads(response.text)
    leagues_list = []
    message = {
        'ru': 'Выберете лигу: ',
        'en': 'Choice a league: '
    }
    for i in leagues:
        leagues_list.append(i.get('id'))

    leagues_list = leagues_list[0:2] + leagues_list[4:6]

    for i, item in enumerate(leagues_list):
        print(i, item)
    choice_league = leagues_list[int(input(message[lang]))]
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
        if counter == 20:
            break

    total_price = round((stat.mean(price_catalog[2:]) + stat.median(price_catalog[2:])) / 2, 4)

    return total_price


lang = get_lang()
get_leagues()

db_file = requests.get(db_url[lang])
with open("bd.pkl", "wb") as code:
    code.write(db_file.content)

with open('bd.pkl', 'rb') as f:
    loaded_dict = pickle.load(f)


def get_list(dic, msg):
    temp_list = [i for i in dic]
    c = 0
    for n, item in enumerate(temp_list):
        print(str(n).ljust(2), item.ljust(29), end=' ')
        c += 1
        if c % 3 == 0:
            print()
    print()
    return temp_list[int(input(msg))]


while True:
    category_message = {
        'ru': 'Выберете раздел: ',
        'en': 'Choice a category: '
    }
    category = get_list(loaded_dict, category_message[lang])
    item_message = {
        'ru': 'Выберете предмет: ',
        'en': 'Choice an item: '
    }
    item = get_list(loaded_dict[category], item_message[lang])
    currency = loaded_dict[category][item]
    count_message = {
        'ru': 'Введите количество: ',
        'en': 'Enter the quantity: '
    }
    count = float(input(count_message[lang]))
    price = get_currency_price(currency)
    total = count * price
    x = count * price
    while int(x) < total:
        count = count - 1
        total = count * price
    print_message = {
        'ru': f'Вы получите {int(total + price)} сфер хаоса за {int(count + 1)}',
        'en': f'You will receive {int(total + price)} orb of chaos for {int(count + 1)}'
    }
    print(print_message[lang])
    print(f"~price {int(total + price)}/{int(count + 1)} chaos", sep="", end='\n\n')
