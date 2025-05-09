import requests
from bs4 import BeautifulSoup
import json
import sqlite3
from data.db_imports import *
from pprint import pprint


def get_names():
    processors = []
    for i in range(1, 19):
        url = f'https://technical.city/en/cpu/rating?&pg={i}'  # сюда ссылку на сайт
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
                    if int(data[5]) > 2018 and data[2] == 'desktop':
                        processors.append(data[1])
                except:
                    pass
        else:
            print(f'Ошибка при загрузке страницы: {response.status_code}')
    return processors


def get_sockets(processors):
    sockets = []
    for processor in processors:
        processor_for_url = processor.replace(' ', '_')
        url = f'https://www.chaynikam.info/{processor_for_url}.html'  # сюда ссылку на сайт
        response = requests.get(url)

        # Проверяем успешность запроса
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            elements = soup.find_all('td', {'class': 'tdc2'})
            try:
                socket = elements[2].get_text()
            except:
                pass
            if socket not in sockets:
                sockets.append(socket)
        else:
            pass
    return sockets


def make_json(sockets):
    sockets_json = {}

    i = 1
    for socket in sockets:
        sockets_json[socket] = i
        i += 1

    # Преобразование словаря в JSON
    json_data = json.dumps(sockets_json, indent=4, ensure_ascii=False)

    # Запись JSON в файл
    with open("data_files/sockets.json", "w", encoding="utf-8") as file:
        file.write(json_data)


def filling_db(current_sockets):
    con = sqlite3.connect("../../db/components.db")
    cur = con.cursor()
    cur.execute("DELETE FROM sockets")
    con.commit()
    con.close()

    db_session.global_init("../../db/components.db")

    db_sess = db_session.create_session()
    for current_socket in current_sockets:
        socket = Sockets()
        socket.name = current_socket
        db_sess.add(socket)
    db_sess.commit()

    sockets = db_sess.query(Sockets).all()

    for socket in sockets:
        print(socket.name)


# обновлять при выходе нового сокета
sockets = get_sockets(get_names())
filling_db(sockets)
make_json(sockets)
