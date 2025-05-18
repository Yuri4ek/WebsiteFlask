import requests
from bs4 import BeautifulSoup
import json
import sqlite3
from data.db_imports import *
from pprint import pprint

# Заголовки для имитации браузера
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}


def get_names():
    # Список для хранения названий материнских плат
    motherboards = []

    # Функция для парсинга одной страницы
    def parse_page(url, page_number=None):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Находим контейнеры с материнскими платами (предположительно div.product-item или li)
                items = soup.find_all('div', class_='uiDeviceCardName')

                for item in items:
                    motherboards.append(item.get_text())
            else:
                print(f"Страница {page_number or 'главная'}: Ошибка {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке страницы {page_number or 'главной'}: {e}")
        except Exception as e:
            print(f"Ошибка при парсинге страницы {page_number or 'главной'}: {e}")

    # Парсинг главной страницы
    base_url = "https://devicelist.best/en/motherboard/"
    parse_page(base_url)

    # Парсинг страниц пагинации (1–6)
    for i in range(1, 7):
        page_url = f"{base_url}page{i}/"
        parse_page(page_url, i)

    return motherboards


def get_info(motherboards_name):
    motherboards_info = []

    base_url = "https://devicelist.best/en/"
    for motherboard_name in motherboards_name:
        name_for_url = motherboard_name.lower().replace(' ', '-')
        response = requests.get(f"{base_url}{name_for_url}/", headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            elements = soup.find_all('td')

            i = 0
            elements_len = len(elements)
            while i < elements_len:
                if 'Socket' in elements[i].get_text():
                    socket = elements[i + 1].get_text()
                    i += 1
                elif 'Chipset' == elements[i].get_text():
                    chipset = elements[i + 1].get_text()
                    i += 1
                elif 'Type of supported memory' in elements[i].get_text():
                    memory_type = elements[i + 1].get_text()
                    i += 1
                elif 'Number of memory slots' in elements[i].get_text():
                    memory_slots = int(elements[i + 1].get_text())
                    i += 1
                elif 'The maximum amount of memory' in elements[i].get_text():
                    try:
                        memory_max = int(elements[i + 1].get_text().split()[0])
                    except:
                        memory_max = None
                    i += 1
                elif 'Number of M. 2 connectors' in elements[i].get_text():
                    m2_quantity = int(elements[i + 1].get_text())
                    i += 1
                elif 'PCI Express Version' in elements[i].get_text():
                    try:
                        pcie_type = int(elements[i + 1].get_text())
                    except:
                        pcie_type = None
                    i += 1
                elif 'Form Factor' in elements[i].get_text():
                    form_factor = elements[i + 1].get_text()
                    i += 1
                i += 1

            motherboards_info.append((motherboard_name, socket, chipset,
                                      memory_type, memory_slots, memory_max,
                                      m2_quantity, pcie_type, form_factor))
    return motherboards_info


def get_prices():
    # Имя JSON-файла
    json_file = "data_files/components_prices.json"

    # Открываем и читаем JSON-файл
    with open(json_file, "r", encoding="utf-8") as file:
        # Загружаем JSON в словарь
        processors_prices = json.load(file)['components']['Материнская плата']
    return processors_prices


def filling_db(motherboards_info):
    # берем сокеты
    with open('data_files/sockets.json', "r", encoding="utf-8") as file:
        sockets = json.load(file)

    # берем типы памяти
    with open('data_files/memory_types.json', "r", encoding="utf-8") as file:
        memory_types = json.load(file)

    # удаляем старые данные
    con = sqlite3.connect("../../db/components.db")
    cur = con.cursor()
    cur.execute("DELETE FROM motherboards")
    con.commit()
    con.close()

    db_session.global_init("../../db/components.db")

    db_sess = db_session.create_session()
    for current_motherboard in motherboards_info:
        motherboard = MotherBoards()
        motherboard.name = current_motherboard[0]
        try:
            modified_socket_name = ''.join(sorted(set(current_motherboard[1].replace(' ', ''))))
            for socket in sockets.keys():
                if modified_socket_name in ''.join(sorted(set(socket))):
                    motherboard.socket_id = sockets[socket]
                    break
        except:
            continue
        motherboard.chipset = current_motherboard[2]
        try:
            motherboard.memory_type_id = memory_types[current_motherboard[3]]
        except:
            motherboard.memory_type_id = None
        motherboard.memory_slots = current_motherboard[4]
        motherboard.memory_max = current_motherboard[5]
        motherboard.m2_quantity = current_motherboard[6]
        motherboard.pcie_type = current_motherboard[7]
        motherboard.form_factor = current_motherboard[8]
        db_sess.add(motherboard)
    db_sess.commit()

    db_sess = db_session.create_session()
    motherBoards = db_sess.query(MotherBoards).all()

    for motherBoard in motherBoards:
        print(motherBoard.name)


def filling_db_prices(motherboards_price):
    db_session.global_init("../../db/components.db")
    db_sess = db_session.create_session()

    # берем данные материнских плат
    motherboards = db_sess.query(MotherBoards).all()

    # удаляем старые данные
    con = sqlite3.connect("../../db/components.db")
    cur = con.cursor()
    cur.execute("DELETE FROM motherboards")
    con.commit()
    con.close()

    # добавляем цены
    for current_motherboard in motherboards:
        motherboard = MotherBoards()
        motherboard.name = current_motherboard.name
        motherboard.socket_id = current_motherboard.socket_id
        motherboard.chipset = current_motherboard.chipset
        motherboard.memory_type_id = current_motherboard.memory_type_id
        motherboard.memory_slots = current_motherboard.memory_slots
        motherboard.memory_max = current_motherboard.memory_max
        motherboard.m2_quantity = current_motherboard.m2_quantity
        motherboard.pcie_type = current_motherboard.pcie_type
        motherboard.form_factor = current_motherboard.form_factor
        price_flag = True
        for motherboard_price in motherboards_price:
            if current_motherboard.name.lower() in motherboard_price[0].lower():
                motherboard.price_in_rubles = motherboard_price[1]
                price_flag = False
                break
        if price_flag:
            motherboard.price_in_rubles = current_motherboard.price_in_rubles
        db_sess.add(motherboard)
    db_sess.commit()

    db_sess = db_session.create_session()
    motherBoards = db_sess.query(MotherBoards).all()

    for motherBoard in motherBoards:
        print(motherBoard.name)


# данные (раз в месяц обновлять)
filling_db(get_info(get_names()))

# цены (раз в день обновлять)
filling_db_prices(get_prices())
