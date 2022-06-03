import requests
from bs4 import BeautifulSoup
import pprint
import json

DOMAIN = "https://www.giftery.ru"

full_list_of_cards=[]
for page in range(1,12):
    url = f"/giftcards?page={page}"
    r=requests.get(DOMAIN+url)
    soup = BeautifulSoup(r.text,'html.parser')
    card_block = soup.find("div","uk-grid uk-child-width-1-1 uk-child-width-1-2@s uk-child-width-1-3@l uk-child-width-1-1 uk-child-width-1-2@s catalog__list-mode-list")

    list = []
    cards_on_page = card_block.findAll("a", class_="gift-card-v2 catalog__list-item gift-card-v2--fill-size gift-card-v2--hover gift-card-v2--shadow")
    print("Пожалуйста, подождите. Идет обработка запроса...")
    for card in cards_on_page:
        dict={}
        name = card.find("div", "gift-card-v2__title").text
        nominal = card.find("div", class_="gift-card-v2__denominations-value").text
        nominal1 = nominal.replace("\xa0"," ")

        link = DOMAIN + card.get("href")
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')
        description = soup.find("div", class_="page-detail-card-brief__content").text
        dict["Наименование карты"] = name
        dict["Описание"] = description
        dict["Номинал"] = nominal1
        dict["Ссылка"] = link
        list.append(dict)

    full_list_of_cards.append(list)

with open("giftcards.txt","w",encoding="utf-8") as f:
    f.write("Список подарочных карт, доступных для приобретения в Интермагазине Giftery")
    json.dump(full_list_of_cards,f, ensure_ascii=False, indent=4)

pprint.pprint(full_list_of_cards)



