import requests
from bs4 import BeautifulSoup
import json
import sqlite3

from data.db_imports import *
from pprint import pprint


def get_names():
    videocards = []
    for i in range(1, 9):
        url = f'https://technical.city/en/video/rating?&pg={i}'  # сюда ссылку на сайт
        response = requests.get(url)

        # Проверяем успешность запроса
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Найдем таблицу с рейтингом процессоров
            table = soup.find('table')

            # Извлекаем заголовки таблицы
            headers = [header.text for header in table.find_all('th')]
            # Извлекаем строки таблицы
            for row in table.find_all('tr')[1:]:  # Пропускаем заголовок
                cols = row.find_all('td')
                data = [col.text.strip() for col in cols]
                try:
                    if int(data[5]) > 2018 and (data[2] == 'desktop' or data[2] == 'workstation'):
                        videocards.append(data[1])
                except:
                    pass
        else:
            print(f'Ошибка при загрузке страницы: {response.status_code}')
    return videocards


def get_info(videocards):
    videocards_info = []
    for videocard in videocards:
        videocard_for_url = videocard.replace(' ', '_')
        url = f'https://www.chaynikam.info/{videocard_for_url}.html'  # сюда ссылку на сайт
        response = requests.get(url)

        # Проверяем успешность запроса
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            elements = soup.find_all('td')

            i = 0
            elements_len = len(elements)
            while i < elements_len:
                if 'Год выхода' == elements[i].get_text():
                    year = int(elements[i + 1].get_text())
                    i += 1
                elif 'Интерфейс' == elements[i].get_text():
                    pcie_type = int(elements[i + 1].get_text().split()[1].split('.')[0])
                    i += 1
                elif 'Объем' == elements[i].get_text():
                    memory_capacity = int(float(elements[i + 1].get_text().split()[0]) / 1000)
                    i += 1
                elif 'Макс. потребляемая энергия (TDP)' == elements[i].get_text():
                    tdp = int(elements[i + 1].get_text().split()[0])
                    i += 1
                i += 1

            videocards_info.append((videocard, year, tdp, memory_capacity, pcie_type))
        else:
            pass
    return videocards_info


def get_prices():
    # Имя JSON-файла
    json_file = "components_prices.json"

    # Открываем и читаем JSON-файл
    with open(json_file, "r", encoding="utf-8") as file:
        # Загружаем JSON в словарь
        videocards_prices = json.load(file)['components']['Видеокарта']
    return videocards_prices


def filling_db(videocards_info):
    # удаляем старые данные
    con = sqlite3.connect("../../db/components.db")
    cur = con.cursor()
    cur.execute("DELETE FROM videocards")
    con.commit()
    con.close()

    db_session.global_init("../../db/components.db")

    db_sess = db_session.create_session()
    for current_videocard in videocards_info:
        videocard = Videocards()
        videocard.name = current_videocard[0]
        videocard.release_year = current_videocard[1]
        videocard.tdp = current_videocard[2]
        videocard.memory_capacity = current_videocard[3]
        videocard.pcie_type = current_videocard[4]
        db_sess.add(videocard)
    db_sess.commit()

    db_sess = db_session.create_session()
    videocards = db_sess.query(Videocards).all()

    for videocard in videocards:
        print(videocard.name)


def filling_db_prices(videocards_price):
    db_session.global_init("../../db/components.db")
    db_sess = db_session.create_session()

    # берем данные видеокард
    videocards = db_sess.query(Videocards).all()

    # удаляем старые данные
    con = sqlite3.connect("../../db/components.db")
    cur = con.cursor()
    cur.execute("DELETE FROM videocards")
    con.commit()
    con.close()

    for current_videocard in videocards:
        videocard = Videocards()
        videocard.name = current_videocard.name
        videocard.release_year = current_videocard.release_year
        videocard.tdp = current_videocard.tdp
        videocard.memory_capacity = current_videocard.memory_capacity
        videocard.pcie_type = current_videocard.pcie_type
        for videocard_price in videocards_price:
            if current_videocard.name.lower() in videocard_price[0].lower():
                videocard.price_in_rubles = videocard_price[1]
                break
        db_sess.add(videocard)
    db_sess.commit()

    videocards = db_sess.query(Videocards).all()

    for videocard in videocards:
        print(videocard.name)


videocards_info = get_info(get_names())
videocards_price = get_prices()

filling_db(videocards_info)
filling_db_prices(videocards_price)
