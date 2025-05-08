import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from data.db_imports import *
from pprint import pprint

# Заголовки для имитации браузера
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}


def get_info():
    # Список для хранения названий материнских плат
    air_coolers = []

    # Функция для парсинга одной страницы
    def parse_page(url, page_number=None):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                products = soup.find_all('div', class_='catalog_item')
                for product in products:
                    # название
                    name_elem = product.find('a',
                                             class_='dark_link js-notice-block__title option-font-bold font_sm')
                    name = ' '.join(name_elem.text.strip().split()[3:])

                    # цена
                    price_elem = product.find('span', class_='price_value')
                    price = price_elem.text.strip()
                    # Clean price to remove non-numeric characters except for decimal point
                    price = int(re.sub(r'[^\d.]', '', price))

                    # tdp
                    tdp = None
                    desc_elem = product.find('div', class_='item_info')
                    if desc_elem:
                        desc_text = desc_elem.text.lower()
                        tdp_match = re.search(r'(\d+)\s*(w|вт|watt)', desc_text)
                        if tdp_match:
                            tdp = int(tdp_match.group(1))
                        elif 'tdp' in desc_text:
                            tdp_match = re.search(r'tdp\s*(\d+)', desc_text)
                            if tdp_match:
                                tdp = int(tdp_match.group(1))
                    if tdp:
                        air_coolers.append((name, tdp, price))
            else:
                print(f"Страница {page_number or 'главная'}: Ошибка {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке страницы {page_number or 'главной'}: {e}")
        except Exception as e:
            print(f"Ошибка при парсинге страницы {page_number or 'главной'}: {e}")

    # Парсинг главной страницы
    base_url = "https://torg-pc.ru/catalog/sistema-vozdushnogo-okhlazhdeniya/filter/clear/"
    parse_page(base_url)

    base_url += "?PAGEN_1="
    # Парсинг страниц пагинации (2-11)
    for i in range(2, 12):
        page_url = f"{base_url}{i}"
        parse_page(page_url, i)

    return air_coolers


def filling_db(coolers_info):
    # удаляем старые данные
    con = sqlite3.connect("../../db/components.db")
    cur = con.cursor()
    cur.execute("DELETE FROM air_coolers")
    con.commit()
    con.close()

    db_session.global_init("../../db/components.db")

    db_sess = db_session.create_session()
    for current_cooler in coolers_info:
        air_cooler = AirCoolers()
        air_cooler.name = current_cooler[0]
        air_cooler.tdp = current_cooler[1]
        air_cooler.price_in_rubles = current_cooler[2]
        db_sess.add(air_cooler)
    db_sess.commit()

    db_sess = db_session.create_session()
    airCoolers = db_sess.query(AirCoolers).all()

    for airCooler in airCoolers:
        print(airCooler.name)


filling_db(get_info())
